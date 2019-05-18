from util.json import register_type
import importlib
import sys, inspect
import pkgutil


JSON_SERIALIZABLE_MODULES = [
    'core.model'
]

def register_json_classes():
    for json_mod in JSON_SERIALIZABLE_MODULES:
        package = importlib.import_module(json_mod)
        for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                              prefix=package.__name__ + '.',
                                                              onerror=lambda x: None):
            mod = importlib.import_module(modname)
            classes = inspect.getmembers(mod, inspect.isclass)
            for class_name, class_type in classes:
                register_type(class_type)

def init():
    register_json_classes()