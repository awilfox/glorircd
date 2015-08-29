# -*- coding: utf-8 -*-
# Copyright © 2015 by the GlorIRCd team.  All rights reserved.
# See COPYING file included with this source for more information.

"""Basic user management for GlorIRCd."""


from taillight.signal import Signal


will_connect_signal = Signal(('core/user', 'will_connect'))
"""The signal fired when a new user connects.  Return False from it to deny the
connection."""


connected_signal = Signal(('core/user', 'connected'))
"""The signal fired when a new user is connected."""


class User:
    """The user."""


class UserManager:
    def __init__(self, server):
        self.server = server

    def introduce_user(self, ip, hostname=None, tls=False):
        """Prepare a :py:class:`User` object for a new connection.

        :param str ip:
            The IP address of the user.

        :param str hostname:
            The hostname of the user (rDNS of the IP).  If ``None``, will be
            looked up.

        :param bool tls:
            Whether or not the user is connecting via TLS.

        :returns:
            If the user should not be allowed to connect, ``None``.  The
            connection must be immediately terminated.  Otherwise, the new
            :py:class:`User` object that corresponds to the user.
        """

        


M_NAME = 'user'
M_CATEGORY = 'core'
M_DESCRIPTION = 'Handles basic user management.'
M_VERSION = '1.0.0'
M_REQUIRES = []
M_CLASS = UserManager
