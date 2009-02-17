# Inspired by Recipe 576609: Non-invasive Dependency Injection - http://code.activestate.com/recipes/576609/
import logging
from errors import *
from common import *

class IoC:
    __instance = None

    def __init__(self):
        self.instances = {}

    @staticmethod
    def reset():
        IoC.__instance = None
    
    @staticmethod
    def get_instance():
        if IoC.__instance == None:
            IoC.__instance = IoC()
            
        return IoC.__instance
    
    @staticmethod
    def configure(config):
        IoC.get_instance().config = config
    
    @staticmethod
    def resolve(cls, *args, **kwargs):
        """Resolves an instance of the specified class.
        If arguments are specified they are used to instantiate the given class.
        If keyword arguments are specified they are used to instantiate any class in the dependency tree that uses them (by name).
        
        Examples:
        IoC.resolve(A) #A depends on B, that depends on C. All of them will get built in runtime.
        IoC.resolve(A,B()) #A depends on B. A will get built using an empty instance of B
        IoC.resolve(A, title="Some Title") #A depends on B, that depends on title. 
                                           #This way B gets built using the overriden title instead 
                                           #of the one configured in the IoC container. This is useful to create custom instances.
                                           #Notice that if your instance has already been loaded before with a different value you need to call IoC.reset()
        
        """
        container = IoC.get_instance()
        if getattr(container, "config", None) == None:
            raise ConfigureError("The container has not yet been configured. Try calling IoC.configure first passing a valid configure source.")
        
        instance = container._instantiate("", cls, args, kwargs)
        container.instances[cls] = instance
        return instance
    
    def _instantiate(self, name, factory, factory_args, factory_kw):
        if not callable(factory):
            logging.debug("Property %r: %s", name, factory)
            return factory

        orig_kwargs = self._prepare_kwargs(factory, factory_args, factory_kw)
        
        argument_list = get_argdefaults(factory)
        kwargs = dict([(key, orig_kwargs[key]) for key in orig_kwargs.keys() if key in argument_list.keys()])
            
        logging.debug("Property %r: %s(%s, %s)", name, factory.__name__,
                factory_args, kwargs)
            
        return factory(*factory_args, **kwargs)
    
    def _get(self, property, factory, factory_args, factory_kw):
        """Lookups the given property name in context.
        Raises KeyError when no such property is found.
        """
        if property not in self.config.components:
            raise KeyError("No factory for: %s", property)

        if property in self.instances:
            return self.instances[property]

        component, args, kwargs = self.config.components[property]
        
        #args = args + factory_args
        kwargs = merge_dicts(factory_kw, kwargs)
        
        instance = self._instantiate(property, *(component, args, kwargs))
        self.instances[property] = instance
        return instance


    def _prepare_kwargs(self, factory, factory_args, factory_kw):
        """Returns keyword arguments usable for the given factory.
        The factory_kw could specify explicit keyword values.
        """
        defaults = get_argdefaults(factory, len(factory_args))

        for arg, default in defaults.iteritems():
            if arg in factory_kw:
                continue
            elif arg in self.config.components:
                defaults[arg] = self._get(arg, factory, factory_args, factory_kw)
            elif default is NO_DEFAULT:
                raise KeyError("No factory for arg: %s" % arg)

        defaults.update(factory_kw)
        return defaults