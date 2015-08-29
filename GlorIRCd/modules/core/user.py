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


class UserSession:
    """A session for a user.  A user may have one or more sessions.

    Note that for multi-session capabilities to work, the client should be using
    either DCP framing or use the echo-message IRC capability.
    """
    def __init__(self, backing, frame=DCPFrame):
        self._registered = False
        self._backing = backing
        self._frame = frame

    @property
    def registered(self):
        """Determines whether the session has completed registration or not."""
        return self._registered

    @property
    def framing_discipline(self):
        """Returns the current framing discipline in use by this session."""
        return self._frame

    @framing_discipline.setter
    def set_framing_discipline(self, new_frame):
        """Set this session's framing discipline."""
        # XXX TODO ensure it is a valid framing discipline before setting.
        self._frame = new_frame

    def send(self, message):
        """Send a message to this session."""
        # cast the message to our current framing type
        our_frame = self._frame(message)

        self._backing.send_raw(our_frame.serialise())


class User:
    """The user."""
    def __init__(self, initial_session):
        self._authenticated = False
        self._username = None
        self._nickname = None
        self._sessions = [initial_session]

    @property
    def authenticated(self):
        """Determine whether the user is authenticated or not."""
        return self._authenticated

    def send(self, message):
        """Send a message to all of the user's connected sessions.

        :param message:
            The message to send.  This may be in AbstractFrame, or any specific
            frame type.  It will be automatically cast to whatever the session
            framing discipline is currently.
        """
        for session in self._sessions:
            session.send(message)


class UserManager:
    def __init__(self, server):
        self.server = server
        self.users = {}

    def introduce_session(self, backing, ip, hostname=None, tls=True):
        """Prepare a :py:class:`UserSession` object for a new connection.

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

        return UserSession(backing)

    def authenticate_session(self, session, username, token):
        """Authenticate a :py:class:`UserSession` to a :py:class:`User`.

        :param UserSession session:
            The session being authenticated.

        :param str username:
            The username to use to authenticate the session.

        :param token:
            The token (passphrase, certificate hash, etc) to use as the
            authentication.

        :returns:
            True or False depending on authentication results.

        :effects:
            Will add the session to the User (or create a User with the session
            as the initial session) if authentication succeeds.
        """


M_NAME = 'user'
M_CATEGORY = 'core'
M_DESCRIPTION = 'Handles basic user management.'
M_VERSION = '1.0.0'
M_REQUIRES = []
M_CLASS = UserManager
