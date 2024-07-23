"""
Generic tests that should work for any kind of callable template.
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

class Test_CallableTemplate_Building(unittest.TestCase) :

    """
    Building/instantiating a callable template result in a callable.
    """

    @classmethod
    def setUpClass(cls) -> None:

        class GlobScope :
            with template['N': int, 'T': type] :
                def cb() :
                    ...
 
        cls.GLOB_SCOPE = vars(GlobScope)

    # ---- ---- ---- ----

    def test_callable_template_full_build(self) :
        """
        Fully building a callable template result in a callable.
        To fully build a callable template, a template argument must be given
        for each template parameters.
        Template arguments can be passed by position or by name.
        """
        
        self.assertTrue(
            not isCallableTemplate(self.GLOB_SCOPE["cb"][5, int])
            and not isCallableTemplate(self.GLOB_SCOPE["cb"][5, 'T':int])
            and not isCallableTemplate(self.GLOB_SCOPE["cb"]['N': 5, 'T':int])
            and not isCallableTemplate(self.GLOB_SCOPE["cb"]['T':int, 'N': 5])
        )

    def test_callable_template_partial_build(self) :
        """
        Partially building a callable template result in a more specific
        callable template (with less template parameters).
        """

        self.assertTrue(
            isCallableTemplate(self.GLOB_SCOPE["cb"][5])
            and isCallableTemplate(self.GLOB_SCOPE["cb"]['N': 5])
            and isCallableTemplate(self.GLOB_SCOPE["cb"]['T': int])
        )
    
    # ---- BONUS :

    def test_BONUS__building_with_nonhashable_template_argument(self) :
        """
        Building a callable template with non hashable template argument is possible.
        Therefore no error should be raised when such an instantiation is made.

        In fact, when they are hashable, the callable built is memoized.
        When they aren't hashable, they aren't memoized.
        """

        class GlobScope :
            with template['switcher': dict] :
                def convertTo(name: str) :
                    return switcher[name]
                
        GLOB_SCOPE = vars(GlobScope)

        self.assertTrue(
          not isCallableTemplate(GLOB_SCOPE['convertTo'][{}])
        )

    # ---- Errors :

    def test_SyntaxError__building_with_templateKwarg_before_templateArg(self) :
        """
        Positional template's arguments must precede keyword template's arguments.
        Otherwise the following error is raised :
        >>> SyntaxError: Keyword template argument precedes positional template argument
        """

        with self.assertRaises(SyntaxError) :
            self.GLOB_SCOPE["cb"]['N':1, str]
  
        #Even with wrong order :
        with self.assertRaises(SyntaxError) :
            self.GLOB_SCOPE["cb"]['T':str, 1]


    def test_TypeError__building_with_template_argument_wrong_type(self) :
        """
        Template's arguments must corresponds to the type of the template's
        parameters.
        Otherwise the following error is raised :
        >>> TypeError: '<Parameter Name>' must be of type '<Type Name>'
        """

        with self.assertRaises(TypeError) :
            self.GLOB_SCOPE["cb"]['N':int, 'T':1]
        with self.assertRaises(TypeError) :
            self.GLOB_SCOPE["cb"][int, 'T':1]
        with self.assertRaises(TypeError) :
            self.GLOB_SCOPE["cb"][int, 1]


class Test_CallableTemplate_Calling(unittest.TestCase) :

    @classmethod
    def setUpClass(cls) -> None:

        class GlobScope :
            with template['N': int, 'T': type] :
                def cb() :
                    ...

        cls.GLOB_SCOPE = vars(GlobScope)

    # ---- ---- ---- ----

    def test_fully_built_callable_template_call(self) :
        self.assertTrue(
            succesfullyRan(self.GLOB_SCOPE["cb"]['N':1, 'T':int])
            and succesfullyRan(self.GLOB_SCOPE["cb"][1, 'T':int])
            and succesfullyRan(self.GLOB_SCOPE["cb"][1, int])
        )

    # ---- Errors :

    def test_TypeError__calling_notfully_built_callable_template(self) :
        """
        Callable template must be fully initialised before being called.
        Otherwise the following error is raised :
        >>> TypeError: 'CallableTemplate' object is not callable
        """

        with self.assertRaises(TypeError) :
            self.GLOB_SCOPE["cb"]()
        
        #Even with partially initialised function template :
        with self.assertRaises(TypeError) :
            self.GLOB_SCOPE["cb"]['T':int]()
