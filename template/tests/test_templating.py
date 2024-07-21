"""
Tests asserting that the process of templating works as intended.
"""


import unittest

from template import template
from callable_template import CallableTemplate


# ********************************** Utils *************************************

def isCallableTemplate(obj: object) -> bool :
    return isinstance(obj, CallableTemplate)


# ********************************** Tests *************************************

class Test_Template_Parameterisation(unittest.TestCase) :

    """
    Template parameters must be declared as follow :
    >>> template['parameter_name': parameter_type]
    
    The type of the parameter can be omitted, when it's 'object'.
    
    The type of a parameter can only be an instance of 'type'.
    Support for other kind of type might be added later.
    """

    def test_single_typed_template_param(self) :
        tmpl = template['param': int]
        self.assertTrue(tmpl._template_params == {"param": int})
    
    def test_single_nottyped_template_param(self) :
        tmpl = template['param']
        self.assertTrue(tmpl._template_params == {"param": object})

    def test_mixin_template_params(self) :
        tmpl = template['p1': int, 'p2']
        self.assertTrue(tmpl._template_params == {"p1": int, "p2": object})

    # ---- Errors :

    def test_TypeError__badly_parameterized_template(self) :
        """
        The type of template parameter must be an instance of 'type'.
        Otherwise the following error is raised :
        >>> TypeError: Template is badly parameterized
        
        Support for other kind of type might be added later.
        """

        # Currently the error message is pretty generic.
        # However there is plan to make it more precise.

        with self.assertRaises(TypeError) :
            template['param': 1]


# TODO : Finding another way to simulate a global scope than using a class.
class Test_Template_ScopeInsertion(unittest.TestCase) :

    """
    Templating a callable 'Cb' in a scope 'S' result in a callable template
    bound to the name 'Cb' in the scope 'S'.
    However, altering 'S' is sometime impossible, in funtion for example.
    In this case, the callable template is bound to the name 'Cb'
    in the global scope and deleted once 'S' is closed in order to simulate
    an insertion inside 'S'.
    """

    def test_globalscope_insertion(self) :
        """
        When templating a callable defined inside the global scope,
        the resulting callable template must be in the global scope. 
        """

        class GlobScope :
            with template['param'] :
                def cb() :
                    ...

        GLOB_SCOPE = vars(GlobScope)

        self.assertTrue(
            "cb" in GLOB_SCOPE
            and isCallableTemplate(GLOB_SCOPE["cb"])
        )

    def test_class_localscope_insertion(self) :
        """
        When templating a callable defined inside a class,
        the resulting callable template must only be accessible via the class.
        """

        class C :
            with template['param'] :
                def cb(self) :
                    ...

        self.assertTrue(
            "cb" in vars(C)
            and isCallableTemplate(C.cb)
        )

    def test_function_localscope_insertion(self) :
        """
        When templating a callable defined inside a function,
        the resulting callable template must only be accessible in the function.
        Therefore, modifying the local scope of the function at runtime
        via the frame of the call should do the trick.
        Howerver, the locals of a function's call frame is read-only.

        The solution choosen is to add the callable template to the global scope
        and remove it once the function has returned.
        """

        def f() :
            with template['param'] :
                def cb() :
                    ...

            return cb

        self.assertTrue(
            isCallableTemplate(f())
            and "cb" not in globals() # Bcs the function 'f' has returned.
        )


class Test_CallableTemplate_Declaration(unittest.TestCase) :

    def test_function_template_declaration(self) :

        """Any kind of function should be templatable."""

        class GlobScope :
            with template['param'] :
                def f() :
                    ...

            with template['param'] :
                async def af() :
                    ...

        GLOB_SCOPE = vars(GlobScope)

        self.assertTrue(
            isCallableTemplate(GLOB_SCOPE["f"])
            and  isCallableTemplate(GLOB_SCOPE["af"])
        )

    def test_class_template_declaration(self) :
        class GlobScope :
            with template['param'] :
                class C :
                    ...

        GLOB_SCOPE = vars(GlobScope)

        self.assertTrue(
            isCallableTemplate(GLOB_SCOPE["C"])
        )

    def test_method_template_declaration(self) :
        class C :
            with template['param'] :
                @classmethod
                def class_meth() :
                    ...

            with template['param'] :
                @staticmethod
                def static_meth() :
                    ...

            with template['param'] :
                def meth(self) :
                    ...

        self.assertTrue(
            isCallableTemplate(C.class_meth)
            and isCallableTemplate(C.static_meth)
            and isCallableTemplate(C.meth)
        )

    # ---- BONUS :

    def test_BONUS__support_parameterised_decoraors(self) :
        """
        Everything inside the "with block" of 'template' should be able to
        lookup the template parameters as if they were global variables;
        even parameterised decorator.
        """
        class GlobScope :
            def repeat(n) :
                def _dec(func) :
                    def _inner(*args, **kwargs) :
                        for _ in range(n) :
                            func(*args, **kwargs)
                    return _inner
                return _dec

            with template['N'] :
                @repeat(N)
                def print_message(msg: str) :
                    print(msg)

        GLOB_SCOPE = vars(GlobScope)

        self.assertTrue(
            isCallableTemplate(GLOB_SCOPE["print_message"])
        )

    # ---- Errors :

    def test_SyntaxError__templating_multiple_statements(self) :
        """
        Templating multiple thing at the same time might suggests that
        the template's arguments are linked.
        Therefore, when templating multiple statements, the followig error
        is raised :
        >>> SyntaxError: Multiple statements given.
        """

        with self.assertRaises(SyntaxError) :
            with template['param'] :
                def f() : ...
                a = ...

    def test_SyntaxError__templating_not_callable(self) :
        """
        Only callables can be templated.
        When templating something else the following error is raised :
        >>> SyntaxError: Can only template class/function definition.
        """

        with self.assertRaises(SyntaxError) :
            with template['param'] :
                a = ...


# TODO : Once `test_function_localscope_insertion` pass, removing 'GlobScope' as those features aren't specific to the global scope features.
class Test_Template_Nesting(unittest.TestCase) :

    def test_nesting_in_class_template(self) :
        class GlobScope :
            with template['p1'] :
                class C :
                    with template['p2'] :
                        def cb() :
                            ...

        GLOB_SCOPE = vars(GlobScope)

        self.assertTrue(
            isCallableTemplate(GLOB_SCOPE["C"])
            and isCallableTemplate(GLOB_SCOPE["C"][object()].cb)
        )

    def test_nesting_in_function_template(self) :
        class GlobScope :
            with template['p1'] :
                def f() :
                    with template['p2'] :
                        def cb() :
                            ...

                    # Bcs there is no way to look in a function scope from outside
                    return cb

        GLOB_SCOPE = vars(GlobScope)

        self.assertTrue(
            isCallableTemplate(GLOB_SCOPE["f"])
            and isCallableTemplate(GLOB_SCOPE["f"][object()]())
        )
