import unittest

from template import template


# ********************************** Tests *************************************

class Tests_FunctionTemplate(unittest.TestCase) :

    @classmethod
    def setUpClass(cls) -> None:

        @template['N': int, 'T': type]
        def templatedFunc () :
            print(isinstance(N, T))

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


    def test_TypeError_wrongType_of_template_argument(self) :
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

        def hasRaisedRuntinmeError(expr: str) -> bool :
            try : eval(expr)
            except RuntimeError : return True
            else : return False


        self.assertTrue(hasRaisedRuntinmeError("templatedFunc()"))
        #Even with partially initialised function template :
        self.assertTrue(hasRaisedRuntinmeError("templatedFunc['T':int]()"))
            

    def test_calling_Initialized_functionTemplate(self) :
        """
        The object returned by fully initilaising a function template is a function.
        Therefore, calling it with proper argument doesn't raise any error unexpected errors.
        """

        def hasSuccessfullyRan(expr: str) -> bool :
            #Based on the fact that templatedFunc doesn't naturally raise an error :
            try : eval(expr)
            except Exception : return False
            else : return True

        self.assertTrue(hasSuccessfullyRan("templatedFunc['N':1, 'T':int]()"))
        self.assertTrue(hasSuccessfullyRan("templatedFunc[1, 'T':int]()"))
        self.assertTrue(hasSuccessfullyRan("templatedFunc[1, int]()"))
