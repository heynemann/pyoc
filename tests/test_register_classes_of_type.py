from base_test import *
from pyoc.config import *
from pyoc.errors import *
import os
from test_classes import classes_of_type

class TestRegisterClassesOfType(BaseTest):
    
    def test_should_resolve_all_inheritors(self):
        config = InPlaceConfig()
        config.register_inheritors("all_classes", os.path.join(os.curdir, "test_classes"), classes_of_type.Base)
        
        IoC.configure(config)
        a = IoC.resolve(classes_of_type.AllItems)

        self.assertNotEqual(a, None)
        self.assertEqual(3, len(a.all_classes))
        self.assertEqual("a", a.all_classes[1].title)
    
        classes = [klass.__class__.__name__ for klass in a.all_classes]
        
        assert("Base" in classes)
        assert("InheritorA" in classes)
        assert("InheritorB" in classes)

if __name__ == "__main__":
    unittest.main()
