# -*- coding: utf-8 -*-
# Copyright © 2015 by the GlorIRCd team.  All rights reserved.
# See COPYING file included with this source for more information.

"""The actual main entry point to GlorIRCd."""


from GlorIRCd.config import ConfigurationHive


class Server:
    def __init__(self):
        self.config_hive = ConfigurationHive()

    def serve(self):
        """Actually run the server."""
        pass


if __name__ == "__main__":
    server = Server()
    server.serve()
