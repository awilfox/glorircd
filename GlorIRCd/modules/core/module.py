# -*- coding: utf-8 -*-
# Copyright © 2015 by the GlorIRCd team.  All rights reserved.
# See COPYING file included with this source for more information.

"""The modular module loader for GlorIRCd.

This module handles loading, reloading, and unloading of modules.  You really
shouldn't unload this module unless you really know what you're doing.  ;)
"""


class ModuleHandler:
    def __init__(self, server):
        self.server = server


M_NAME = 'module'
M_CATEGORY = 'core'
M_DESCRIPTION = 'Handles loading, reloading, and unloading of other modules.'
M_VERSION = '1.0.0'
M_REQUIRES = []
M_CLASS = ModuleHandler
