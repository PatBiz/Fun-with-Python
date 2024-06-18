# Used version : CPython 3.12.1


# ********************************* Imports ************************************
from __future__ import annotations

"Standard Library :"
import inspect
#To annotate
from typing import overload
from collections.abc import Sequence, Callable


"Local Library :"
from function_template import FunctionTemplate
#To annotate
from utils.types import TemplateParameter, isTemplateParameter


# ******************************** Constants ***********************************

__all__ = ("template")


# ********************************* Classes ************************************

class template :
    def __init__(self, template_params: dict[str, type]) -> None:
        self.template_params = template_params

    @overload
    @classmethod
    def __class_getitem__(cls, key: TemplateParameter) -> template : ...

    @overload
    @classmethod
    def __class_getitem__(cls, key: Sequence[TemplateParameter]) -> template : ...

    @classmethod
    def __class_getitem__(cls, key) :
        if isTemplateParameter(key) :
            return template({key.start: key.stop})

        if isinstance(key, Sequence) :
            template_params = {}
            for k in key :
                if not isTemplateParameter(k) :
                  raise ValueError("Template is badly parameterized")
                template_params[k.start] = k.stop
            return template(template_params)

        raise ValueError("Template is badly parameterized")

    def __call__(self, func: Callable) -> FunctionTemplate :
        #Getting 'func' declaration :
        whole_declaration_lines, declaration_1st_line = inspect.getsourcelines(func)
        caller_line = inspect.currentframe().f_back.f_lineno

        caller_relative_line = caller_line - declaration_1st_line

        #top_decl = "".join(whole_declaration_lines[:caller_relative_line])
        sub_decl = "".join(whole_declaration_lines[caller_relative_line + 1:])

        return FunctionTemplate(
            func.__name__,
            sub_decl,
            #top_decl,
            self.template_params,
            func.__globals__, #inspect.currentframe().f_back.f_locals,
        )
