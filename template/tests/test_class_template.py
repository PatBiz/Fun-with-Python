"""
More specific tests for class template.
"""


import unittest

from template import template
from callable_template import CallableTemplate


# ********************************** Utils *************************************

def isCallableTemplate(obj: object) -> bool :
    return isinstance(obj, CallableTemplate)


def succesfullyRan(cb) :
    # Based on the assumption that 'cb' doesn't naturally raise an error.
    try : cb()
    except Exception : return False
    else : return True


# ********************************** Tests *************************************

# TODO : Testing class template
