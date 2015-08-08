# -*- coding: utf-8 -*-
# Copyright © 2015 by the GlorIRCd team.  All rights reserved.
# See COPYING file included with this source for more information.

"""The actual main entry point to GlorIRCd."""


from logging import getLogger
from taillight.signal import Signal

from GlorIRCd.config import ConfigurationHive
from GlorIRCd.core import bootstrap_load


class Server:
    def __init__(self):
        self.config_hive = ConfigurationHive()
        self.modules = {}
        self.mod_inst = {}
        self.logger = getLogger(__name__)
        #bootstrap_load(self, 'core.module')

    def register_command_handler(self, cmd_or_numeric, handler):
        """Register a handler for a command or numeric.

        :param cmd_or_numeric:
            The command or numeric that this handler desires to receive.

        :param handler:
            A callable that will receive notifications when the specified
            command or numeric is sent/received.
        """

        self.logger.debug("Registering %r as handler for %s", handler,
                          cmd_or_numeric)
        Signal(cmd_or_numeric).add(handler)

    def serve(self):
        """Actually run the server."""
        pass


if __name__ == "__main__":
    server = Server()
    server.serve()
