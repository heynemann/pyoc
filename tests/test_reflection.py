import unittest
import sys
import os
root_path = os.path.abspath(__file__ + "/../../")
sys.path.insert(0, root_path)
import pyoc.reflection as ref

def return_something():
    return "something"

class TestReflection(unittest.TestCase):
    def setUp(self):
        self.module_path = os.path.join(os.path.split(__file__)[0], "test_reflection.py")
    
    def test_reflection_get_module_from_path(self):
        module = ref.get_module_from_path(self.module_path)
        assert(module.__name__ == "test_reflection")
        assert(module.return_something() == "something")
        
    def test_get_classes_for_module(self):
        classes = ref.get_classes_for_module(ref.get_module_from_path(self.module_path))
        assert(type(classes) == list)
        assert(len(classes) == 1)
        assert(classes[0].__name__ == TestReflection.__name__)
        assert(classes[0].return_something() == "something else")

    @staticmethod
    def return_something():
        return "something else"
        
    def local_return_something(self):
        return "yet something else"
        
    def test_get_methods_for_class(self):
        methods = ref.get_methods_for_class(TestReflection)
        assert(type(methods) == list)
        assert(len(methods) > 0)
        func = getattr(self, "local_return_something") 

        assert(func.__name__ in [f.__name__ for f in methods])
        assert(func() == "yet something else")
        
    def some_random_method(self, arg1, arg2 = "default", arg3 = "default2", *args, **kwargs):
        pass
        
    def test_get_arguments_with_defaults_for_method(self):
        arguments_with_defaults, var_args, var_kwargs = ref.get_arguments_for_method(getattr(self, "some_random_method"))
        
        assert(type(arguments_with_defaults) == dict)
        assert(len(arguments_with_defaults) == 3)
        assert("self" not in arguments_with_defaults)
        assert("arg1" in arguments_with_defaults)
        assert("arg2" in arguments_with_defaults)
        assert("arg3" in arguments_with_defaults)

        assert("args" == var_args)
        assert("kwargs" == var_kwargs)

        assert(arguments_with_defaults["arg1"] == None)
        assert(arguments_with_defaults["arg2"] == "default")
        assert(arguments_with_defaults["arg3"] == "default2")
    
    def test_get_class_in_module(self):
        klass = ref.get_class_for_module(ref.get_module_from_path(self.module_path), "TestReflection")
        assert(klass.__name__ == TestReflection.__name__)
        assert(klass.return_something() == "something else")
        
if __name__ == '__main__':
    unittest.main()
