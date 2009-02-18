from common import *
from errors import *
import sys

class BaseConfig(object):
    def __init__(self):
        """Creates empty context.
        """
        self.components = {}
    
    def assert_not_cyclical_dependency(self, property, component):
        component_args = get_argdefaults(component).keys()
        for component_arg in component_args:
            if self.components.has_key(component_arg):
                parent_component = self.components[component_arg][0]
                parent_args = get_argdefaults(parent_component).keys()
                if property in parent_args:
                    raise CyclicalDependencyError("There is a cyclical dependency between %s and %s. Cyclical dependencies are not supported yet!"
                                                  % (component.__name__, parent_component.__name__))
        

class InPlaceConfig(BaseConfig):

    def __init__(self):
        super(InPlaceConfig, self).__init__()

    
    def register(self, property, component, *args, **kwargs):
        if (args or kwargs) and not callable(component):
            raise ValueError(
                    "Only callable component supports extra args: %s, %s(%s, %s)"
                    % (property, component, args, kwargs))

        if callable(component): self.assert_not_cyclical_dependency(property, component)
        self.components[property] = "direct", component, args, kwargs

    def register_files(self, property, root_path, pattern):
        all_classes = []
        for module_path in locate("*_action.py", root=root_path):
            module_name = os.path.splitext(os.path.split(module_path)[-1])[0]
            sys.path.insert(0,os.path.abspath(root_path))
            
            module = __import__(module_name)
            
            class_name = camel_case(module.__name__)
            cls = getattr(module, class_name, None)
            
            if cls == None:
                raise AttributeError("The class %s could not be found in file %s. Please make sure that the class has the same name as the file, but Camel Cased."
                                     % (class_name, module_name))
            
            all_classes.append(cls)
            
        
        self.components[property] = "indirect", all_classes, None, None
        