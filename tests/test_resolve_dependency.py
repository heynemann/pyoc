from base_test import *
from pyoc.config import *

class TestResolveDependencies(BaseTest):
    
    def test_should_resolve_dependency(self):
        expected_title = "some weird title"
        
        config = InPlaceConfig()
        config.register("b", B)
        config.register("c", C)
        config.register("title", expected_title)
        
        IoC.configure(config)
        a = IoC.resolve(A)
        
        self.assertNotEqual(a, None)
        self.assertNotEqual(a.b, None)
        self.assertEqual(B, a.b.__class__)
        self.assertEqual(expected_title, a.b.title)
        
    
    def test_should_resolve_dependency_with_extra_argument(self):
        fake_expected_title = "some weird title"
        expected_title = "real title"
        
        config = InPlaceConfig()
        config.register("b", B)
        config.register("c", C)
        config.register("title", fake_expected_title)
        
        IoC.configure(config)
        
        b = B(expected_title)
        a = IoC.resolve(A, b)
        
        self.assertNotEqual(a, None)
        self.assertNotEqual(a.b, None)
        self.assertEqual(B, a.b.__class__)
        self.assertEqual(expected_title, a.b.title)
        
    def test_should_resolve_dependency_with_keyword_argument(self):
        fake_expected_title = "some weird title"
        expected_title = "real title"
        
        config = InPlaceConfig()
        config.register("b", B)
        config.register("c", C)
        config.register("title", fake_expected_title)
        
        IoC.configure(config)
        
        a = IoC.resolve(A, title = expected_title)
        
        self.assertNotEqual(a, None)
        self.assertNotEqual(a.b, None)
        self.assertNotEqual(a.c, None)
        self.assertEqual(B, a.b.__class__)
        self.assertEqual(C, a.c.__class__)
        self.assertEqual(expected_title, a.b.title)
        self.assertEqual(expected_title, a.c.title)
        
    def test_should_resolve_nested_dependencies(self):
        expected_title = "Test Title"
        
        config = InPlaceConfig()
        config.register("e", E)
        config.register("f", F)
        config.register("title", expected_title)
        
        IoC.configure(config)
        
        d = IoC.resolve(D)
        
        self.assertNotEqual(d, None)
        self.assertNotEqual(d.e, None)
        self.assertNotEqual(d.e.f, None)
        self.assertEqual(E, d.e.__class__)
        self.assertEqual(F, d.e.f.__class__)
        self.assertEqual(expected_title, d.e.f.title)
    
    def test_should_resolve_cyclical_dependency(self):
        expected_title = "Test Title"
        
        config = InPlaceConfig()
        config.register("parent", CyclicalParent)
        config.register("child", CyclicalChild)
        config.register("title", expected_title)
        
        IoC.configure(config)
        
        self.assertRaises(CyclicalDependencyError, IoC.resolve, CyclicalParent)

        #self.assertNotEqual(parent, None)
        #self.assertNotEqual(parent.child, None)
        #self.assertEqual(CyclicalParent, parent.__class__)
        #self.assertEqual(CyclicalChild, parent.child.__class__)
        #self.assertEqual(expected_title, parent.child.title)
        
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