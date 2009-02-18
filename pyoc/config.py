import common
import os
from errors import *
import sys

class BaseConfig(object):
    allowed_lifestyle_types = ("transient", "singleton",)
    
    def __init__(self, lifestyle_type = "singleton"):
        """Creates empty context.
        """
        self.components = {}
        self.assert_valid_lifestyle_type(lifestyle_type)
        self.default_lifestyle_type = lifestyle_type
        
    def set_default_lifestyle_type(self, lifestyle_type):
        self.assert_valid_lifestyle_type(lifestyle_type)
        self.default_lifestyle_type = lifestyle_type
        
    def assert_valid_lifestyle_type(self, lifestyle_type):
        if lifestyle_type not in BaseConfig.allowed_lifestyle_types:
            raise InvalidLifestyleTypeError("The specified lifestyle type (%s) is not valid. Allowed lifestyle types: %s" %
                                            (lifestyle_type, ",".join(BaseConfig.allowed_lifestyle_types)))
        
    def assert_not_cyclical_dependency(self, property, component):
        component_args = common.get_argdefaults(component).keys()
        for component_arg in component_args:
            if self.components.has_key(component_arg):
                parent_component = self.components[component_arg][2]
                parent_args = common.get_argdefaults(parent_component).keys()
                if property in parent_args:
                    raise CyclicalDependencyError("There is a cyclical dependency between %s and %s. Cyclical dependencies are not supported yet!"
                                                  % (component.__name__, parent_component.__name__))
                
    def register(self, property, component, lifestyle_type = "UNKNOWN", *args, **kwargs):
        if (lifestyle_type == "UNKNOWN"): lifestyle_type = self.default_lifestyle_type
        self.assert_valid_lifestyle_type(lifestyle_type)        
        
        if (args or kwargs) and not callable(component):
            raise ValueError(
                    "Only callable component supports extra args: %s, %s(%s, %s)"
                    % (property, component, args, kwargs))

        if callable(component): self.assert_not_cyclical_dependency(property, component)
        component_definition = ("direct", lifestyle_type, component, args, kwargs,)
        self.components[property] = component_definition
        if callable(component): self.components[component] = component_definition

    def register_files(self, property, root_path, pattern, lifestyle_type = "UNKNOWN"):
        if (lifestyle_type == "UNKNOWN"): lifestyle_type = self.default_lifestyle_type
        self.assert_valid_lifestyle_type(lifestyle_type)        
        
        all_classes = []
        for module_path in common.locate("*_action.py", root=root_path):
            module_name = os.path.splitext(os.path.split(module_path)[-1])[0]
            sys.path.insert(0,os.path.abspath(root_path))
            
            module = __import__(module_name)
            
            class_name = common.camel_case(module.__name__)
            cls = getattr(module, class_name, None)
            
            if cls == None:
                raise AttributeError("The class %s could not be found in file %s. Please make sure that the class has the same name as the file, but Camel Cased."
                                     % (class_name, module_name))
            
            all_classes.append(cls)
        
        component_definition = "indirect", lifestyle_type, all_classes, None, None
        self.components[property] = component_definition

class InPlaceConfig(BaseConfig):
    '''
    Creates a blank configuration for code configuration.
    Pretty useful for unit testing the container and dependencies.
    '''
    def __init__(self):
        super(InPlaceConfig, self).__init__()
    
class FileConfig(BaseConfig):
    '''
    Creates a container using the definitions in the specified file.
    The file MUST be a python module and MUST declara a "def config(container):" function.
    This is the function that will configure the container.
    
    Default file is pyoc_config.py.
    '''
    def __init__(self, filename = "pyoc_config.py", root_path=os.path.abspath(os.curdir)):
        super(FileConfig, self).__init__()
        self.execute_config_file(root_path, filename)
    
    def execute_config_file(self, root_path, filename):
        sys.path.insert(0,root_path)
        module_name = os.path.splitext(filename)[0]
        module = __import__(module_name)
        func = getattr(module, "config")
        config_helper = FileConfig.ContainerConfigHelper(self)
        func(config_helper)
    
    class ContainerConfigHelper(object):
        def __init__(self, file_config):
            self.file_config = file_config
            
        def register(self, property, component, *args, **kwargs):
            self.file_config.register(property, component, *args, **kwargs)
            
        def register_files(self, property, root_path, pattern):
            self.file_config.register_files(property, root_path, pattern)