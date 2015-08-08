# -*- coding: utf-8 -*-
# Copyright © 2015 by the GlorIRCd team.  All rights reserved.
# See COPYING file included with this source for more information.

"""Contains the core exceptions for the GlorIRCd daemon.

Note that you must derive from ModuleError in this class to ensure that any
raises are caught correctly by the daemon.  Otherwise you will just core and
everyone will hate you.  :)
"""


class BaseError(Exception):
    """The base GlorIRCd exception.  DO NOT INHERIT FROM THIS."""
    pass


class ConfigError(BaseError):
    """Raised when a configuration option is missing or invalid."""
    pass


class ModuleError(BaseError):
    """The base GlorIRCd exception class for module-defined exceptions.

    You should inherit from this.
    """
    pass


class VersionError(BaseError):
    """Raised when the running version of GlorIRCd doesn't match a desired
    module or server."""
    pass
