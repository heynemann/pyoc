import logging
import os, fnmatch

NO_DEFAULT = "NO_DEFAULT"

def get_argdefaults(factory, num_skipped=0):
    """Returns dict of (arg_name, default_value) pairs.
    The default_value could be NO_DEFAULT
    when no default was specified.
    """
    args, defaults = _getargspec(factory)

    if defaults is not None:
        num_without_defaults = len(args) - len(defaults)
        default_values = (NO_DEFAULT,) * num_without_defaults + defaults
    else:
        default_values = (NO_DEFAULT,) * len(args)

    return dict(zip(args, default_values)[num_skipped:])

def _getargspec(factory):
    """Describes needed arguments for the given factory.
    Returns tuple (args, defaults) with argument names
    and default values for args tail.
    """
    import inspect
    if inspect.isclass(factory):
        factory = factory.__init__

    #logging.debug("Inspecting %r", factory)
    
    args, vargs, vkw, defaults = inspect.getargspec(factory)
    if inspect.ismethod(factory):
        args = args[1:]
    return args, defaults

def merge_dicts(priority_dict, other_dict):
    new_dict = {}
    
    for key, value in other_dict.items():
        new_dict[key] = value
    
    for key, value in priority_dict.items():
        new_dict[key] = value
        
    return new_dict

def locate(pattern, root=os.curdir):
    root_path = os.path.abspath(root)
    for path, dirs, files in os.walk(root_path):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

def camel_case(module_name):
        names = module_name.split("_")
        newName = []
        for name in names:
            newName.append(name[:1].upper() + name[1:])
        return "".join(newName)