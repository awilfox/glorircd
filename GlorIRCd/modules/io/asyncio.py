# -*- coding: utf-8 -*-
# Copyright © 2015 by the GlorIRCd team.  All rights reserved.
# See COPYING file included with this source for more information.

"""The AsyncIO backend for GlorIRCd."""

import asyncio
from logging import getLogger
import os.path
import ssl
from taillight.signal import Signal

from GlorIRCd.errors import ConfigError, ModuleError
from GlorIRCd.modules.core.module import can_unload_signal


default_ciphers = """ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!3DES:!MD5:!PSK"""


class GlorIRCdClientProtocol(asyncio.Protocol):
    def connection_made(self):
        pass


class AsyncioBackend:

    """The AsyncIO backend module for GlorIRCd."""

    def __init__(self, server):
        self.server = server
        self.logger = getLogger('io/asyncio')

        if 'io/asyncio' not in self.server.config_hive.mod_config:
            raise ConfigError('No asyncio configuration found.')

        # deep copy, so that we can compare changes later.
        self.config = dict(self.server.config_hive.mod_config['io/asyncio'])

        self.loop = asyncio.get_event_loop()
        self.servers = []

        bind_addrs = self.config.get('bind', '::').split(',')
        if 'plain' in self.config:
            plain_ports = self.config['plain'].split(',')
        else:
            plain_ports = []

        if 'ssl' in self.config:
            ssl_ports = self.config['ssl'].split(',')

            self.context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            self.context.options |= ssl.OP_NO_SSLv2
            self.context.options |= ssl.OP_NO_SSLv3
            self.context.options |= ssl.OP_NO_TLSv1
            self.context.set_ciphers(self.config.get('ssl_ciphers',
                                                    default_ciphers))
            def_path = os.path.join(self.server.config_hive.path,
                                    'dhparams.pem')
            self.context.load_dh_params(self.config.get('dh_params_path',
                                                        def_path))
        else:
            ssl_ports = []

        for addr in bind_addrs:
            for port in plain_ports:
                num = int(port.strip())
                srv = self.loop.create_server(GlorIRCdClientProtocol, addr, num)
                self.servers.append(srv)
                self.loop.run_until_complete(srv)
            for port in ssl_ports:
                num = int(port.strip())
                srv = self.loop.create_server(GlorIRCdClientProtocol, addr, num,
                                              ssl=self.context)
                self.servers.append(srv)
                self.loop.run_until_complete(srv)

        # Prevent the backend from being unloaded.
        can_unload_signal.add(lambda fqmn: False, listener='io/asyncio')

        self.server.io_serve = self.loop.run_forever


M_NAME = 'asyncio'
M_CATEGORY = 'io'
M_DESCRIPTION = 'Provides the AsyncIO I/O backend.'
M_VERSION = '1.0.0'
M_REQUIRES = []
M_CLASS = AsyncioBackend
