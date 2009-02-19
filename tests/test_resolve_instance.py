from base_test import *
from pyoc.config import *
from pyoc.errors import *

class TestResolveInstance(BaseTest):
    
    def test_should_resolve_dependency(self):
        expected_title = "some weird title"
        
        config = InPlaceConfig()
        some_b = B("other title")
        config.register_instance("b", some_b)
        config.register("c", C)
        config.register("title", expected_title)
        
        IoC.configure(config)
        a = IoC.resolve(A)
        
        self.assertNotEqual(a, None)
        self.assertNotEqual(a.b, None)
        self.assertEqual(some_b, a.b)
        self.assertEqual("other title", a.b.title)
        self.assertEqual(expected_title, a.c.title)
        
    def test_should_resolve_instance_dependency(self):
        expected_title = "some weird title"
        
        config = InPlaceConfig()
        some_f = F("other title")
        config.register("e", E)
        config.register_instance("f", some_f)
        
        IoC.configure(config)
        d = IoC.resolve(D)
        
        self.assertNotEqual(d, None)
        self.assertNotEqual(d.e, None)
        self.assertNotEqual(d.e.f, None)
        self.assertEqual(d.e.f, some_f)
        self.assertEqual(d.e.f.title, "other title")
        
class A:
    def __init__(self, b, c):
        self.b = b
        self.c = c
    
class B:
    def __init__(self, title):
        self.title = title
        
class C:
    def __init__(self, title):
        self.title = title
        
class D:
    def __init__(self, e):
        self.e = e 

class E:
    def __init__(self, f):
        self.f = f
        
class F:
    def __init__(self, title):
        self.title = title

class CyclicalParent():
    def __init__(self, child):
        self.child = child

class CyclicalChild():
    def __init__(self, parent):
        self.parent = parent

if __name__ == "__main__":
    unittest.main()