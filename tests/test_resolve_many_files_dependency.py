from base_test import *
from pyoc.config import *
from pyoc.errors import *

class TestResolveManyFilesDependency(BaseTest):
    
    def test_should_resolve_files_in_path(self):
        expected_title = "some weird title"
        fake_title = "fake"
        
        config = InPlaceConfig()
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_classes"))
        
        config.register_files("actions", root_path, "*_action.py")
        config.register("b", B)
        config.register("c", C)
        config.register("title", fake_title)
        
        IoC.configure(config)
        actions = IoC.resolve_all("actions", title = expected_title)
        
        self.assertNotEqual(actions, None)
        self.assertEqual(len(actions), 3)
        
        self.assertEqual(actions[0].__class__.__name__, "AAction")
        self.assertEqual(actions[1].__class__.__name__, "DAction")
        self.assertEqual(actions[2].__class__.__name__, "EAction")
        
        for i in range(3):
            self.assertEqual(expected_title, actions[i].b.title)
            self.assertEqual(expected_title, actions[i].c.title)

class B:
    def __init__(self, title):
        self.title = title
        
class C:
    def __init__(self, title):
        self.title = title
        
if __name__ == "__main__":
    unittest.main()