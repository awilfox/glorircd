# -*- coding: utf-8 -*-
# Copyright © 2015 by the GlorIRCd team.  All rights reserved.
# See COPYING file included with this source for more information.

class AsyncioBackend:
    def __init__(self, server):
        self.server = server

M_NAME = 'asyncio'
M_CATEGORY = 'io'
M_DESCRIPTION = 'Provides the AsyncIO I/O backend.'
M_VERSION = '1.0.0'
M_CLASS = AsyncioBackend
