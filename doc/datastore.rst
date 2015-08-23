=================================
GlorIRCd Data Store Specification
=================================
:Authors:
  * **Andrew Wilcox**
  * **Elizabeth Myers**
:Version:
  1.0
:Status:
  Draft
:Copyright:
  © 2015.  NCSA open source licence.


This document describes the high-level architecture for the GlorIRCd Data Store,
and its public API.




Groups (channels)
=================

A **group**, sometimes referred to a *channel* or *room*, is a place for people
to connect, hold conversations, and share information together.  This is of
course the cornerstone of any multi-user chat system.

When a group is created in GlorIRCd, it is by default a "temporary" group
(unless automatic persistence is enabled).  When all members of the group have
left, the group ceases to exist.  Persisting (or registering) a group allows
details about the group to persist even when no members are joined to it.



Group types
-----------

There are three main group types in GlorIRCd, two of which are supported by the
Data Store.


Temporary groups
````````````````

A **temporary group** is a group that does not persist.  Since it does not
persist, it is not supported by the Data Store.


Permanent groups
````````````````

A **permanent group** is a group that persists even when no users are joined to
it.  This is similar to a "ChanServ guarded channel" on traditional IRC
networks serviced by Shaltúre, Anope, and similar services packages.


Carried groups
``````````````

A **carried group** is a group from another network that is relayed to the
current network.  Certain details about carried groups are saved locally to
ensure security and performance, but not all details are saved as the current
network is not the group's home.



Group metadata
--------------

This section describes the metadata of groups that are saved to the Data Store.


Name
````

The name of the group.

:Type: String.

:Maximum length: Depends on compatibility level.  200 ASCII characters in IRC
                 1459 mode; 50 ASCII characters in IRC 2812 mode;
                 user-configurable number of Unicode characters in native mode.

:Permanent Type: Yes.  Required.

:Carried Type: Yes.  Required.


Topic
`````

The topic of the group.

:Type: String.

:Maximum length: Depends on compatibility level.  ???  390 characters is cited
                 in ircv3-harmony, use this for 1459 mode?

:Permanent Type: Yes.  Optional, can be unset.

:Carried Type: No.


URL
```

The URL of the group.  The meaning of the URL is group-dependent, but is
typically a Web address of the group's home page, or perhaps an FTP site where
you can download software if it is a software development group.

:Type: Well-formed URI as defined by [RFC3986]_.

:Maximum length: 255 characters.

:Permanent Type: Yes.  Optional, can be unset.

:Carried Type: Yes.


Owner
`````

The owner of the group.  For a permanent group, this is a reference to a local
user (and can therefore be dereferenced by querying the Data Store for the
specified user).  For a carried group, this is a reference to the foreign user
that owns the group and is *not* the local contact for this group.

:Type: Local or foreign User reference.

:Permanent Type: Yes.  Required.

:Carried Type: Yes.  Required.


Successor
`````````

The successor to the owner of the group.  If the owner's user account is
disabled or deleted, the successor will be promoted to the owner.

:Type: Local User reference.

:Permanent Type: Yes.  Optional, but recommended.  Can be unset.

:Carried Type: No.


Contact
```````

The contact of the carried group.  This is a local user that is considered to
be authoritative for the relaying of the carried group to the local network.

:Type: Local User reference.

:Permanent Type: No.

:Carried Type: Yes.  Required.


Founded
```````

The date and time this group was founded.  Some legacy IRC clients may care.
Otherwise this is just for user enjoyment.  The server itself does not use this
parameter for any reason.

:Type: UTC Timestamp.

:Permanent Type: Yes.  Only an administrator with the special permission
                 ``network/rewrite_history`` (or working knowledge of SQL) can
                 change this value.

:Carried Type: No.



Group properties
----------------

This section describes the properties of groups that are saved to the Data
Store.  Note that properties can be either On or Off, and apply only to
permanent groups.  They are never stored for carried or temporary groups.


private
```````

This property determines if the group is hidden from lists of group, such as a
network-wide list of active group, or a list of groups to which a specific user
is currently joined.

:Default: On.

:MODE: p


invite-only
```````````

This property determines if the group is in an "invite only" mode.  Only users
with the ``group/join`` permission may join the group if this property is set.

:Default: Off.

:MODE: i




Users
=====

A **user** is an entity that connects to a GlorIRCd server to use it for
communicating.  A user could be a living being or an automated script that
serves information at the request of another user.

A **local user** is an entity that has their registration on the network that a
specific GlorIRCd server is participating on, while a **foreign user** is an
entity that has their registration on another network.  A network may choose to
allow authentication from other networks, and may choose to allow other networks
to authenticate users using its user database.  More information about these
features is available in the GlorIRCd Operator's Guide.

Networks may choose to disallow unauthenticated or "guest" users from connecting
to the network.  Registrations may be performed using the REGISTER command if
allowed by the network, or may be added by an administrator via API or other
administrative commands.



User metadata
-------------

This section describes the metadata of users that are saved to the Data Store.


Account name
````````````

The account name of the user, used during sign on and in ACLs.  Note that this
may or may not be the same as the user's current alias/nickname.

:Type: String.

:Maximum length: Depends on compatibility level.  9 ASCII characters in IRC 1459
                 and 2812 modes; user-configurable number of Unicode characters
                 in native mode.

:Required: Yes.


Real name
`````````

The user's "real life" name.  This field *should* be used for the user's legal
name, but this cannot be enforced in software for obvious reasons.

:Type: String.

:Maximum length: 255 Unicode characters.

:Required: No, but highly recommended for compatibility with IRC clients.  This
           will simply default to the account name if none is specified.


Nicknames
`````````

The registered nicknames (also known as *aliases*, *pseudonyms*, and *handles*)
of the user.  Other users may not use these nicknames.

:Type: Array of String.

:Maximum length: Depends on compatibility level.  At IRC 1459/2812 levels, a
                 user may have up to 5 nicknames registered, each with 9 ASCII
                 characters each.  In native mode, the number of nicknames per
                 account and the length of each nickname are user-configurable.

:Required: At least one nickname is required.




ACLs
====

The GlorIRCd Data Store also contains the **access control lists**, or **ACLs**,
for groups and users.  ACLs can be thought of as permission lists, or "ChanServ
FLAGS/ACCESS" on traditional services-based IRC networks.

For information on the supported permissions in GlorIRCd, see the GlorIRCd
Security Manual.




A word on modules
=================

The metadata, properties, and permissions described in this document are the set
of data that comprises the core of GlorIRCd, and is guaranteed to be available
in all GlorIRCd installations.  Additional modules, supplied with GlorIRCd
and/or written by third parties, may add additional metadata, properties, and/or
permissions.  For more information about data added by modules, please read the
documentation included with any module(s) you install.




Citations
=========

.. [RFC1459] Oikarinen, Reed. "`Internet Relay Chat Protocol.`_" RFC 1459. IETF,
             May 1993. Web. 22 Aug 2015.

.. [RFC2812] Kalt, C. "`Internet Relay Chat: Client Protocol.`_" RFC 2812. IETF,
             Apr 2000. Web. 22 Aug 2015.

.. [RFC3986] Berners-Lee, et al. "`Uniform Resource Identifier (URI): Generic
             Syntax.`_" RFC 3986. IETF, Jan 2005. Web. 22 Aug 2015.

.. _`Internet Relay Chat Protocol.`: http://tools.ietf.org/html/rfc1459

.. _`Internet Relay Chat: Client Protocol.`: http://tools.ietf.org/html/rfc2812

.. _`Uniform Resource Identifier (URI): Generic Syntax.`:
   http://tools.ietf.org/html/rfc3986
