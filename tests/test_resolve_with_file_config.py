from base_test import *
from pyoc.config import *
from pyoc.errors import *

class TestResolveWithFileConfig(BaseTest):
    
    def test_should_resolve_dependency(self):
        expected_title = "Some Weird Title"
        
        config = FileConfig("test1_config.py")
        
        IoC.configure(config)
        a = IoC.resolve(A)
        
        self.assertNotEqual(a, None)
        self.assertNotEqual(a.b, None)
        self.assertEqual("B", a.b.__class__.__name__)
        self.assertEqual(expected_title, a.b.title)
        
    
    def test_should_resolve_dependency_with_extra_argument(self):
        expected_title = "real title"
        
        config = FileConfig("test2_config.py")
        
        IoC.configure(config)
        
        b = B(expected_title)
        a = IoC.resolve(A, b)
        
        self.assertNotEqual(a, None)
        self.assertNotEqual(a.b, None)
        self.assertEqual(B, a.b.__class__)
        self.assertEqual(expected_title, a.b.title)
        
    def test_should_resolve_dependency_with_keyword_argument(self):
        expected_title = "real title"
        
        config = FileConfig("test2_config.py")
        
        IoC.configure(config)
        
        a = IoC.resolve(A, title = expected_title)
        
        self.assertNotEqual(a, None)
        self.assertNotEqual(a.b, None)
        self.assertNotEqual(a.c, None)
        self.assertEqual("B", a.b.__class__.__name__)
        self.assertEqual("C", a.c.__class__.__name__)
        self.assertEqual(expected_title, a.b.title)
        self.assertEqual(expected_title, a.c.title)
        
    def test_should_resolve_nested_dependencies(self):
        expected_title = "Test Title"
        
        config = FileConfig("test3_config.py")
        
        IoC.configure(config)
        
        d = IoC.resolve(D)
        
        self.assertNotEqual(d, None)
        self.assertNotEqual(d.e, None)
        self.assertNotEqual(d.e.f, None)
        self.assertEqual("E", d.e.__class__.__name__)
        self.assertEqual("F", d.e.f.__class__.__name__)
        self.assertEqual(expected_title, d.e.f.title)
    
    def test_should_resolve_with_default_config(self):
        expected_title = "Some Weird Title"
        
        config = FileConfig()
        
        IoC.configure(config)
        a = IoC.resolve(A)
        
        self.assertNotEqual(a, None)
        self.assertNotEqual(a.b, None)
        self.assertEqual("B", a.b.__class__.__name__)
        self.assertEqual(expected_title, a.b.title)
        
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

if __name__ == "__main__":
    unittest.main()