# ********************************* Imports ************************************
from __future__ import annotations

"Standard Library :"
#To annotate :
from typing import TypeGuard


# ********************************** Types *************************************

# --- Template's parameter :

type TemplateParameter = slice[str, type] | str

def isTemplateParameter(obj) -> TypeGuard[TemplateParameter] :
    try :
        return (
            isinstance(obj.start, str)
            and isinstance(obj.stop, type)
            and obj.step is None
        )
    except AttributeError :
        return isinstance(obj, str)


# --- Template's argument :

type TemplateArg = object
type TemplateKwarg = slice[str, TemplateArg]

def isTemplateArg(obj) -> TypeGuard[TemplateArg] :
    # As 'isinstance(obj.stop, object)' is always true
    return True

def isTemplateKwarg(obj) -> TypeGuard[TemplateKwarg] :
    try :
        return (
            isinstance(obj.start, str)
           #and isinstance(obj.stop, object)  # <-- Always true
            and obj.step is None
        )
    except AttributeError :
        return False
