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