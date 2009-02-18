from base_test import *
from pyoc.config import *
from pyoc.errors import *

class TestDifferentLifestyleTypes(BaseTest):
    
    def test_should_resolve_as_singleton(self):
        config = InPlaceConfig()
        config.register("b", B)
        config.register("title", "Some Title")
        
        IoC.configure(config)
        a = IoC.resolve(A)

        a.b.title = "Other title"
        
        b = IoC.resolve(B)
        
        self.assertNotEqual(b, None)
        self.assertEqual(b, a.b)
        self.assertEqual(b.title, "Other title")
    
    def test_should_resolve_as_transient(self):
        config = InPlaceConfig()
        config.set_default_lifestyle_type("transient")
        config.register("b", B)
        config.register("title", "Some Title")
        
        IoC.configure(config)
        
        a = IoC.resolve(A)

        a.b.title = "Other title"
        
        b = IoC.resolve(B)
        
        self.assertNotEqual(b, None)
        self.assertNotEqual(b, a.b)
        self.assertEqual(b.title, "Some Title")
        self.assertEqual(a.b.title, "Other title")
        

    def test_should_resolve_as_transient_by_component(self):
        config = InPlaceConfig()
        config.register("b", B2)
        config.register("c", C2, "transient")
        config.register("title", "Some Title")
        
        IoC.configure(config)
        a = IoC.resolve(A2)

        a.b.title = "Other title"
        a.c.title = "Other title"
        
        b = IoC.resolve(B2)
        c = IoC.resolve(C2)
        
        self.assertNotEqual(b, None)
        self.assertEqual(b, a.b)
        self.assertEqual(b.title, "Other title")
        self.assertNotEqual(c, a.c)
        self.assertEqual(c.title, "Some Title")
        
class A:
    def __init__(self, b):
        self.b = b
    
class B:
    def __init__(self, title):
        self.title = title

class A2:
    def __init__(self, b, c):
        self.b = b
        self.c = c
    
class B2:
    def __init__(self, title):
        self.title = title
        
class C2:
    def __init__(self, title):
        self.title = title

if __name__ == "__main__":
    unittest.main()