# -*- coding: utf-8 -*-
# Copyright © 2015 by the GlorIRCd team.  All rights reserved.
# See COPYING file included with this source for more information.

"""This module contains the very core methods of GlorIRCd that cannot be
modularised and must be present for sanity.

If you aren't sure if something should go in here or not, it shouldn't.
"""


from importlib import import_module

from GlorIRCd.errors import ModuleError
import GlorIRCd.modules
from GlorIRCd.util.conditions import precondition


@precondition(lambda modname: modname is not None and modname != '')
def bootstrap_load(server, modname):
    """Load a module (bootstrap version).

    This serves as the module loader during early initialisation when we don't
    yet have the module loader loaded (as it, itself, is a module).

    :param server:
        The server instance that is loading the module.

    :param str modname:
        The name of the module to load.

    :effects:
        The module will be loaded.

    :raises ValueError:
        If no module with that name exists.

    :raises :py:exc:`~GlorIRCd.errors.ModuleError`:
        If the module raises a ModuleError.

    :raises :py:exc:`~GlorIRCd.errors.VersionError`:
        If the module and the running version of GlorIRCd conflict.

    :returns:
        The module's name.  This can never return None.
    """

    mod = import_module(modname, 'GlorIRCd.modules')
    if mod.M_NAME in server.modules:
        raise ModuleError("This module has already been loaded.")
    server.modules[mod.M_NAME] = mod
