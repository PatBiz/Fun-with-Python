# ********************************* Imports ************************************
from __future__ import annotations

"Standard Library :"
#To annotate :
from typing import TypeGuard, Any


# ********************************** Types *************************************

# --- Template's parameter :

type TemplateParameter = slice[str, type]

def isTemplateParameter(obj) -> TypeGuard[TemplateParameter] :
    try :
        return (
            isinstance(obj.start, str)
            and isinstance(obj.stop, type)
            and obj.step is None
        )
    except AttributeError :
        return False


# --- Template's argument :

type TemplateArg = Any
type TemplateKwarg = slice[str, TemplateArg]

def isTemplateArg(obj) -> TypeGuard[TemplateArg] :
    return True  # As it always return 'True' I won't use it.

def isTemplateKwarg(obj) -> TypeGuard[TemplateKwarg] :
    try :
        return isinstance(obj.start, str) and obj.step == None
    except AttributeError :
        return False
