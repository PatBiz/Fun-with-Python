import unittest

from template import template


# ********************************** Tests *************************************

class Tests_FunctionTemplate(unittest.TestCase) :

    @classmethod
    def setUpClass(cls) -> None:

        @template['N': int, 'T': type]
        def templatedFunc () :
            return isinstance(N, T)

        globals()["templatedFunc"] = templatedFunc

    def test_SyntaxError_templateKwarg_before_templateArg(self) :
        """
        Keywords template's argument cannot preceed positional templat's arguments.
        Otherwise the following error is raised :
        >>> SyntaxError: Keyword template argument precedes positional template argument
        """

        def hasRaisedSyntaxError(expr: str) -> bool :
            try : eval(expr)
            except SyntaxError : return True
            else : return False

        self.assertTrue(hasRaisedSyntaxError("templatedFunc['N':1, str]"))
        #Even with wrong order :
        self.assertTrue(hasRaisedSyntaxError("templatedFunc['T':str, 1]"))


    def test_TypeError_wrongType_templateArgument(self) :
        """
        Template's arguments must corresponds to the type of the template's parameters.
        Otherwise the following error is raised :
        >>> TypeError: '<Parameter Name>' must be of type '<Type Name>'
        """

        def hasRaisedTypeError(expr: str) -> bool :
            try : eval(expr)
            except TypeError : return True
            else : return False

        self.assertTrue(hasRaisedTypeError("templatedFunc['N':int, 'T':1]"))
        self.assertTrue(hasRaisedTypeError("templatedFunc[int, 'T':1]"))
        self.assertTrue(hasRaisedTypeError("templatedFunc[int, 1]"))


    def test_RuntimeError_calling_NotFullyInitialized_functionTemplate(self) :
        """
        Functions templates must be fully initialised before calling them.
        Otherwise the following error is raised :
        >>> RuntimeError: Object of type 'FunctionTemplate' aren't callable.
        ... You must fully initialise it, before calling it.
        """

        def hasRaisedRuntimeError(expr: str) -> bool :
            try : eval(expr)
            except RuntimeError : return True
            else : return False


        self.assertTrue(hasRaisedRuntimeError("templatedFunc()"))
        #Even with partially initialised function template :
        self.assertTrue(hasRaisedRuntimeError("templatedFunc['T':int]()"))


    def test_calling_Initialized_functionTemplate(self) :
        """
        The object returned by fully initilaising a function template is a function.
        Therefore, properly built functions don't raise unexpected errors.
        """

        def hasSuccessfullyRan(expr: str) -> bool :
            #Based on the fact that 'templatedFunc' doesn't naturally raise an error :
            try : eval(expr)
            except Exception : return False
            else : return True

        self.assertTrue(hasSuccessfullyRan("templatedFunc['N':1, 'T':int]()"))
        self.assertTrue(hasSuccessfullyRan("templatedFunc[1, 'T':int]()"))
        self.assertTrue(hasSuccessfullyRan("templatedFunc[1, int]()"))


class Tests_FunctionTemplate_NonHashableTemplateArgument(unittest.TestCase) :

    @classmethod
    def setUpClass(cls) -> None:

        @template['switcher': dict]
        def convertTo(name: str) :
            return switcher[name]

        globals()["convertTo"] = convertTo

    def test_calling_Initialized_functionTemplate(self) :
        """
        Template's arguments aren't needed to be hashable.
        However, when they are hashable, the function built is memoized.
        Therefore, functions built with non hashable arguments don't raise unexpected errors.
        """

        def hasSuccessfullyRan(expr: str) -> bool :
            #Based on the fact that 'convertTo' doesn't naturally raise an error :
            try : eval(expr)
            except Exception : return False
            else : return True

        self.assertTrue(hasSuccessfullyRan("convertTo['switcher': {'a': 1}]('a')"))
        self.assertTrue(hasSuccessfullyRan("convertTo[{'a': 1}]('a')"))
