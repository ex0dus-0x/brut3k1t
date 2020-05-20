"""
manager.py

    Defines the plugin manager architecture for brute, which helps manage over
    pre-existing modules, plus the provisioning and addition of any new plugin modules.
"""

import os
import glob
import imp


class BruteManager(object):
    def __init__(self):
        pass

    def stats(self):

    def get_module(self, name):
        pass

    def new_module(self, name, path):
        pass

    def add_module(self, path):
        pass
