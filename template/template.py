# Used version : CPython 3.12.1


# ********************************* Imports ************************************
from __future__ import annotations

"Standard Library :"
import ast
import inspect
import sys

from itertools import islice
from textwrap import dedent
#To annotate
from typing import overload
from collections.abc import Sequence

"Local Library :"
from callable_template import CallableTemplate
#To annotate
from utils.types import TemplateParameter, isTemplateParameter


# ******************************** Constants ***********************************

__all__ = ("template")


# ********************************* Classes ************************************

class template :
    def __init__(self, template_params: dict[str, type]) -> None :
        self._template_params = template_params

        try :
            self._frame = sys._getframe(2)
        except AttributeError as err :
            # Might occurs if the Python implementation used doesn't support
            # frames objects.
            raise RuntimeError("'sys' module couldn't be used to get frame.")


    @overload
    @classmethod
    def __class_getitem__(cls, key: TemplateParameter) -> template : ...

    @overload
    @classmethod
    def __class_getitem__(cls, key: Sequence[TemplateParameter]) -> template : ...

    @classmethod
    def __class_getitem__(cls, key) :

        # TODO : Making error messages more useful when badly parameterising 'template'

        if isTemplateParameter(key) :
            if isinstance(key, str) :
                return template({key: object})
            return template({key.start: key.stop})

        if isinstance(key, Sequence) :
            template_params = {}
            for k in key :
                if not isTemplateParameter(k) :
                  raise TypeError("Template is badly parameterized")
                if isinstance(k, str) :
                    template_params[k] = object
                else :
                    template_params[k.start] = k.stop
            return template(template_params)

        raise TypeError("Template is badly parameterized")


    def _get_WithBlock(self) -> str :
        with_block_start, with_block_end, *_ = next(islice(
            self._frame.f_code.co_positions(),
            self._frame.f_lasti // 2,
            None,
        ))
        return dedent("".join(
            inspect.findsource(self._frame)[0][
                with_block_start : with_block_end
            ]
        ))

    def _silence_WithBlock(self) :
        sys.settrace(lambda frame, event, arg : None)
        self._frame.f_trace = lambda frame, event, arg : exec("raise Exception")

    def __enter__(self) :

        with_block = self._get_WithBlock()

        stmts = ast.parse(with_block).body

        if len(stmts) != 1 :
            # Otherwise, it suggests that the template's arguments are linked.
            raise SyntaxError("Multiple statements given.")

        def_stmt = stmts[0]

        CallableDef = ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef
        if not isinstance(def_stmt, CallableDef) :
            # Even if variable template does exist in C++, it's rarely used
            # and would be confusing in Python.
            # Thus, the choice to forbid it.
            raise SyntaxError("Can only template class/function definition.")

        cb_template = CallableTemplate(
            def_stmt.name,
            with_block,
            self._template_params,
            self._frame.f_globals,
        )

        self._frame.f_locals[def_stmt.name] = cb_template

        if def_stmt.name not in self._frame.f_locals :
            # Might not happen on all Python implementations.
            # But, in CPython, function namespaces were changed for performance
            # reason, making 'frame.f_locals' a dictionary created on the fly.
            # Therefore any updates to 'frame.f_locals' may not happen.
            # (See : https://peps.python.org/pep-0667/#rationale)
            #
            # Btw, PEP 667 might solve this problem in Python 3.13.
            raise NotImplementedError("To be implemented.")

        self._silence_WithBlock()

    def __exit__(self, exc_type, exc_value, traceback) :
        return True
