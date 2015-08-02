# -*- coding: utf-8 -*-
# Copyright © 2015 by the GlorIRCd team.  All rights reserved.
# See COPYING file included with this source for more information.

"""This module contains the very core methods of GlorIRCd that cannot be
modularised and must be present for sanity.

If you aren't sure if something should go in here or not, it shouldn't.
"""

from glorircd.util.conditions import Precondition


@precondition(lambda modname: modname is not None and modname != '')
def bootstrap_load(modname):
    """Load a module (bootstrap version).

    This serves as the module loader during early initialisation when we don't
    yet have the module loader loaded (as it, itself, is a module).

    :param str modname:
        The name of the module to load.

    :effects:
        The module will be loaded.

    :raises ValueError:
        If no module with that name exists.

    :raises :py:exc:`~GlorIRCd.errors.VersionError`:
        If the module and the running version of GlorIRCd conflict.

    :returns:
        None.
    """

    pass