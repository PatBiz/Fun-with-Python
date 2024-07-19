# ********************************* Imports ************************************
from __future__ import annotations

"Standard Library :"
from textwrap import dedent
from functools import lru_cache
#To annotate :
from collections.abc import Sequence, Callable
from typing import overload, Any

"Local Library :"
from utils.frozendict import frozendict
#To annotate :
from utils.types import (
    TemplateArg, isTemplateArg,
    TemplateKwarg, isTemplateKwarg,
)


# ********************************* Classes ************************************

class CallableTemplate :
    def __init__(
        self,
        name: str,
        declaration: str,
        template_params:dict[str, type],
        globals: dict[str, Any]
    ) -> None :
        self._name = name
        self._declaration = declaration
        self._template_params = template_params
        self._globals = globals


    @overload
    def __getitem__(self, key: TemplateArg | TemplateKwarg) -> Callable : ...

    @overload
    def __getitem__(self, key: Sequence[TemplateArg | TemplateKwarg]) -> Callable : ...

    def _computeTemplateArg(self, template_arg: TemplateArg, pos: int) :
        param_name = list(self._template_params.keys())[pos]
        param_type = self._template_params[param_name]

        if not isinstance(template_arg, param_type) :
            raise TypeError(f"'{param_name}' must be of type '{param_type}'.")
        return param_name, template_arg

    def _computeTemplateKwarg(self, template_kwarg: TemplateKwarg) :
        param_name = template_kwarg.start
        arg = template_kwarg.stop

        try :
            param_type = self._template_params[param_name]
        except KeyError :
            raise RuntimeError(f"'{param_name}' isn't a template parameter.")

        if not isinstance(arg, param_type) :
            raise TypeError(f"'{param_name}' must be of type '{param_type}'.")
        return param_name, arg

    def __getitem__(self, key) :
        build_args = {}

        if isinstance(key, Sequence) :
            met_kwarg = False
            for i,k in enumerate(key) :
                if isTemplateKwarg(k) :
                    comp = self._computeTemplateKwarg(k)
                    build_args[comp[0]] = comp[1]
                    met_kwarg = True
                    continue
                if not met_kwarg and isTemplateArg(k) :
                    comp = self._computeTemplateArg(k, i)
                    build_args[comp[0]] = comp[1]
                    continue
                raise SyntaxError(
                    "Keyword template argument precedes positional template argument"
                )
            return self._build(frozendict(build_args))

        if isTemplateKwarg(key) :
            comp = self._computeTemplateKwarg(key)
            build_args[comp[0]] = comp[1]
            return self._build(frozendict(build_args))

        # 'key' is of type 'TemplateArg'
        comp = self._computeTemplateArg(key, 0)
        build_args[comp[0]] = comp[1]
        return self._build(frozendict(build_args))


    def _build(self, build_args: frozendict) -> Callable|CallableTemplate :
        try :
            hash(build_args)
        except TypeError :
            return self._notCached_build(build_args)
        else :
            return self._cached_build(build_args)

    def _notCached_build(self, build_args: frozendict) -> Callable|CallableTemplate :
        template_scope = build_args.unfreeze()

        isBeingPartiallyBuild = len(self._template_params) > len(template_scope)
        if isBeingPartiallyBuild :
            return CallableTemplate(
                self._name,
                self._declaration,
                {
                    k:v
                    for k,v in self._template_params.items()
                    if k not in template_scope
                },
                self._globals | template_scope
            )

        template_scope |= self._globals
        exec(dedent(self._declaration), template_scope)
        return template_scope[self._name]

    @lru_cache(50)
    def _cached_build(self, build_args: frozendict) -> Callable|CallableTemplate :
        return self._notCached_build(build_args)


    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise RuntimeError(
            "Object of type 'CallableTemplate' aren't callable.\n"
            "You must fully specialize/initialise it."
        )
