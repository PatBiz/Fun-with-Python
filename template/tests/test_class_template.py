import unittest

from template import template


# ********************************** Tests *************************************

# --- Unit Test :: Function template :

class ClassTemplate_Tests(unittest.TestCase) :

    @classmethod
    def setUpClass(cls) -> None:

        @template['N': int, 'T': type]
        class TemplatedClass :
            ...

        globals()["TemplatedClass"] = TemplatedClass
