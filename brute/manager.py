"""
manager.py

    Defines the plugin manager architecture for brute, which helps manage over
    pre-existing modules, plus the provisioning and addition of any new plugin modules.
"""

import os
import inspect
import pkgutil
import pathlib
import importlib
import typing as t

from brute.core.base import BruteBase

# type alias to the main module tree
Modules = t.Dict[str, t.Dict[str, t.Type[BruteBase]]]


class BruteManager(object):
    """
    Module manager that internally handles all the modules in the local registry.
    """

    @staticmethod
    def _parse_mods(modtype: str) -> t.Dict[str, t.Type[BruteBase]]:
        """
        Helper method for parsing out all the modules with a BruteBase grandparent
        class given a specific module type.

        :type modtype: str module type
        """

        # TODO: make this better!
        namespace = f"brute.modules.{modtype}"

        # get directory path to module type
        curr = os.path.dirname(__file__)
        mod_dir = os.path.join(curr, "modules", modtype)
        pkg_dir = pathlib.Path(mod_dir).resolve()

        #print(pkg_dir)

        # modules to return
        mods: t.Dict[str, t.Type[BruteBase]] = {}

        # get all modules with a BruteBase parent class
        for (_, mod, _) in pkgutil.iter_modules([pkg_dir]):

            # initialize submodule name to inspect
            modname = f"{namespace}.{mod}"
            #print(modname)

            module = importlib.import_module(modname)

            # look through all attributes, and return only the plugin
            # with the BruteBase grandparent subclass
            for name in dir(module):
                attribute = getattr(module, name)

                # check if class, and if the grandparent type is BruteBase
                if inspect.isclass(attribute):

                    # TODO: make better!
                    try:
                        grandparent = attribute.__bases__[0].__bases__[0]
                        if grandparent is BruteBase:
                            mods[attribute.name] = attribute
                    except IndexError:
                        pass

        return mods


    def __init__(self):
        """
        Creates a mapping of all dynamically imported plugins for interaction.
        """

        # initializes a mapping for each module type to each module name and instance
        self.modules: Modules = dict(
            map(lambda x: (x, BruteManager._parse_mods(x)),
            ["web", "protocol"]
        ))

        # total number of modules, for returning stats
        self.total_modules: int = sum(len(v) for _, v in self.modules.items())


    @property
    def stats(self) -> str:
        """
        Returns a string to output with brute module stats, including total count, plus each module organized
        by module type.
        """
        stat_str = f"\nTotal Number of Modules: {self.total_modules}\n\nAvailable Modules:\n\n"
        for t, entries in self.modules.items():
            stat_str += f"  {t.capitalize()} Modules:\n"
            for k, _ in entries.items():
                stat_str += f"    * {k}\n"
            stat_str += "\n"
        return stat_str


    @property
    def modtypes(self) -> t.List[str]:
        """
        Returns all the module types supported by brute.
        """
        return self.modules.keys()


    def get_module(self, name: str) -> t.Optional[t.Type[BruteBase]]:
        """
        Given a name, find the corresponding module in the existing mapping. Return None if
        it doesn't exist.

        :type name: name of module to find
        """
        for _, mods in self.modules.items():
            for n, mod in mods.items():
                if n == name:
                    return mod

        return None


    def new_module(self, modtype, name, path):
        """
        Initializes a new plugin module script, but does not add to the existing mapping to
        local registry and plugin folder.
        """
        pass


    def add_module(self, path):
        """
        Given a plugin module path, attempt to dynamically import it, and add it to existing mapping
        to local registry and plugin folder.
        """
        self.modules[modtype][name] = {}
        pass
