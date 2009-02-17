from common import *
from errors import *

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
        self.components[property] = component, args, kwargs
