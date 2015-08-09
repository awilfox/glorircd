# -*- coding: utf-8 -*-
# Copyright © 2015 by the GlorIRCd team.  All rights reserved.
# See COPYING file included with this source for more information.

"""The modular module loader for GlorIRCd.

This module handles loading, reloading, and unloading of modules.  You really
shouldn't unload this module unless you really know what you're doing.  ;)
"""


from logging import getLogger
from taillight.signal import Signal


can_load_signal = Signal(('core/module', 'can_load'))
"""The Signal fired to determine if a module can be loaded or not."""


loaded_signal = Signal(('core/module', 'loaded'))
"""The Signal fired when a new module has been loaded."""


can_unload_signal = Signal(('core/module', 'can_unload'))
"""The Signal fired to determine if a module can be unloaded or not."""


unloaded_signal = Signal(('core/module', 'unloaded'))
"""The Signal fired when a module has been unloaded."""


class ModuleHandler:
    def __init__(self, server):
        self.server = server
        self.server.register_command_handler('modload',
                                             self.load_from_irc)
        self.server.register_command_handler('modreload',
                                             self.reload_from_irc)
        self.server.register_command_handler('modunload',
                                             self.unload_from_irc)
        self.logger = getLogger(__name__)

        # Load modules from the configuration hive.
        for module in self.server.config_hive.modules:
            self.load_module(module)

    def load_module(self, modname):
        """Load a module into GlorIRCd.

        :param str modname:
            The name of the module to load.

        :returns:
            The name of the module loaded, or None if no module was loaded.
        """

        self.logger.debug("Discovering module '%s'...", modname)

        modname.replace('/', '.')

        mod = None
        try:
            mod = __import__('GlorIRCd.modules.{}'.format(modname), globals(),
                             locals(), [modname], 0)
        except ImportError:
            try:
                mod = __import__('{}'.format(modname), globals(), locals(),
                                 [modname], 0)
            except ImportError:
                pass

        if mod is None:
            self.logger.error("Module '%s' was not found.", modname)
            return None

        fqmn = '{category}/{name}'.format(category=mod.M_CATEGORY,
                                          name=mod.M_NAME)
        self.logger.debug("Loading module '%s' with API version %s (%s)...",
                          fqmn, mod.M_VERSION, mod.M_DESCRIPTION)

        if fqmn in self.server.modules:
            self.logger.debug("Not loading already loaded module '%s'.", fqmn)
            return None

        if not all(can_load_signal.call(fqmn)):
            self.logger.debug("Module '%s' cannot be loaded due to server "
                              "policy.", fqmn)
            return None

        self.server.modules[fqmn] = mod
        self.server.mod_inst[fqmn] = mod.M_CLASS(self.server)

        loaded_signal.call(fqmn)

        self.logger.debug("Loaded module '%s'.", fqmn)
        return fqmn

    def load_from_irc(self, caller, line):
        """Load a module from a connected user.

        :param caller:
            The user that ran the command.

        :param line:
            The line of the command.

        :line_format:
            Expected parameters: [modname] or [category, name].
        """

        if caller.has_acl('server/loadmodule'):
            if len(line.params) == 2:
                return self.load_module("{}.{}".format(*line.params))
            elif len(line.params) == 1:
                return self.load_module(line.params[0])
            else:
                pass  # XXX handle Invalid Syntax
        else:
            pass  # XXX handle Not Permitted

    def reload_from_irc(self, caller, line):
        """Reload a module from a connected user.

        :param caller:
            The user that ran the command.

        :param line:
            The line of the command.

        :line_format:
            Expected parameters: [modname] or [category, name].
        """

        if self.unload_from_irc(caller, line):
            self.load_from_irc(caller, line)

    def unload_from_irc(self, caller, line):
        pass

M_NAME = 'module'
M_CATEGORY = 'core'
M_DESCRIPTION = 'Handles loading, reloading, and unloading of other modules.'
M_VERSION = '1.0.0'
M_REQUIRES = []
M_CLASS = ModuleHandler
