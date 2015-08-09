# -*- coding: utf-8 -*-
# Copyright © 2015 by the GlorIRCd team.  All rights reserved.
# See COPYING file included with this source for more information.

"""The actual main entry point to GlorIRCd."""


from logging import basicConfig, getLogger
from taillight.signal import Signal

from GlorIRCd.config import ConfigurationHive
from GlorIRCd.core import bootstrap_load


class Server:
    """The GlorIRCd server.

    :ivar config_hive:
        The :py:class:`~GlorIRCd.config.ConfigurationHive` instance for this
        server.

    :ivar modules:
        The dict containing the raw module handles.

    :ivar mod_inst:
        The dict containing the actual module instances.

    :ivar _logger:
        The root logger.  Don't touch.

    :ivar io_serve:
        The method to call from :py:meth:`serve` to actually run the server.
        This is set by the currently active I/O backend module.
    """

    def __init__(self):
        basicConfig(level='DEBUG')

        self.config_hive = ConfigurationHive()
        self.modules = {}
        self.mod_inst = {}
        self._logger = getLogger("GlorIRCd daemon core")
        self.io_serve = lambda: None

        bootstrap_load(self, 'core.module')

    def register_command_handler(self, cmd_or_numeric, handler):
        """Register a handler for a command or numeric.

        :param cmd_or_numeric:
            The command or numeric that this handler desires to receive.

        :param handler:
            A callable that will receive notifications when the specified
            command or numeric is sent/received.
        """

        if isinstance(cmd_or_numeric, str):
            command = cmd_or_numeric.upper()
        else:
            command = str(cmd_or_numeric)

        self._logger.debug("Registering %r as handler for %s", handler, command)
        Signal(('command', command)).add(handler)

    def serve(self):
        """Actually run the server.  This is not expected to return."""

        self.io_serve()


if __name__ == "__main__":
    server = Server()
    server.serve()
