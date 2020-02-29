import sys
import importlib
from types import ModuleType
from threading import Lock

# all accesses to sys.modules must be programmed to acquire this lock first
sys_mod_lock = Lock()


def deep_reload(m: ModuleType):
    # https://stackoverflow.com/questions/42870428/deep-reload-modules-from-only-one-package#answer-42870429
    def _reload(m: ModuleType):
        name = m.__name__  # get the name that is used in sys.modules
        name_ext = name + '.'  # support finding sub modules or packages
        del m

        def compare(loaded: str):
            return (loaded == name) or loaded.startswith(name_ext)

        # prevent changing iterable while iterating over it
        all_mods = tuple(sys.modules)
        sub_mods = filter(compare, all_mods)

        # remove sub modules and packages from import cache
        for pkg in sub_mods:
            del sys.modules[pkg]

        return importlib.import_module(name)

    with sys_mod_lock:
        return _reload(m)
