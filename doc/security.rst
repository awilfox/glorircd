========================
GlorIRCd Security Manual
========================
:Authors:
  * **Andrew Wilcox**
  * **Elizabeth Myers**
:Version:
  1.0
:Status:
  Draft
:Copyright:
  © 2015.  NCSA open source licence.


This document describes the security features of GlorIRCd, first from a user's
perspective, then from an operator's perspective, and finally from a developer's
perspective.




User security
=============

This chapter describes the user-facing security features of GlorIRCd.  You will
learn about permissions, ACLs, alternative authentication methods, TLS 1.2, best
practices, and so much more!



Permissions and ACLs
--------------------

This section describes **permissions**, the ability to perform an action on a
GlorIRCd network, and **access control lists** or **ACLs**, a list of
permissions that applies to a specific entity.

If you are familiar with traditional IRC services packages, a group ACL can be
thought of as similar to - yet much more powerful than - ChanServ FLAGS.

Most permissions signify that a user can perform a specific action to a group,
another user, or the network itself.  For instance, the ``group/kick``
permission will allow you to "kick" (remove) another user from the group on
which you have that permission.  However, there are some permissions that will
*prevent* you from performing an action.  The ``group/ban`` permission signifies
that the specified user cannot join a group.

In this document, the **target** of a permission is the user that has that
permission assigned to them on a specified ACL.


Group permissions
`````````````````

This section describes the group permissions available in the core of GlorIRCd.
Additional "modules" (bits of functionality) loaded by your network's operators
may add additional permissions.  For more information about those, you can
search online for the GlorIRCd Master Module Directory.


``group/ban``
~~~~~~~~~~~~~

This permission prevents the target from joining the group.


``group/join``
~~~~~~~~~~~~~~

This permission allows the target to join the group.  This is useful mainly in
either of the following scenarios:

* The group has the "invite only" property set; only people specifically marked
  with this permission will be allowed to join.

* A moderator has banned a large IP range or an entire ISP - perhaps a bunch of
  users from AOL were spamming the group - and they want to allow certain users
  from that ISP to be able to join even though the ISP itself is banned.

  Note that the most specific permission always wins, so an ISP ban would be
  able to be "overridden" by a user-specific join permission.


``group/kick``
~~~~~~~~~~~~~~

This permission allows the target to "kick" (remove) other users from the group.


``group/metadata``
~~~~~~~~~~~~~~~~~~

This is a nested permission that defines what metadata, if any, the target can
change for the group.  Examples of metadata are the group's URL and the topic of
the group.

It can be granted as ``group/metadata/TAG`` (where TAG is the metadata that the
target can modify), or ``group/metadata/*`` to allow the target to modify all
group metadata.


``group/mute``
~~~~~~~~~~~~~~

This permission prevents the target from speaking to the group.


``group/property``
~~~~~~~~~~~~~~~~~~

This permission allows the target to set properties of the group, such as
whether the group is private or not.


User permissions
````````````````

This section describes the user permissions available in the core of GlorIRCd.
Additional "modules" (bits of functionality) loaded by your network's operators
may add additional permissions.  For more information about those, you can
search online for the GlorIRCd Master Module Directory.


``user/block``
~~~~~~~~~~~~~~

This permission prevents the target from messaging the specified user.


``user/message``
~~~~~~~~~~~~~~~~

This permission allows the target to message the specified user.  For instance,
if Alice has set the "invisible" mode on herself, but has given Bob the
``user/message`` permission, he will be able to message her anyway.


Network permissions
```````````````````

This section describes network permissions available in the core of GlorIRCd.
These permissions are used to grant users administrative privileges on networks,
so they may or may not be applicable to you.  Additional "modules" (bits of
functionality) loaded by your network's operators may add additional
permissions.  For more information about those, you can search online for the
GlorIRCd Master Module Directory.


``network/debug``
~~~~~~~~~~~~~~~~~

This permission allows the target to use special debug commands, including
viewing internal counters and modifying internal settings.  This should only be
used when absolutely necessary as it can be potentially hazardous.


``network/inject``
~~~~~~~~~~~~~~~~~~~~~~~~~~

This permission allows the target to manually inject a command into the network.
This permission should **never be used under any circumstance**.


``network/kill``
~~~~~~~~~~~~~~~~

This permission allows the target to "kill" (forcibly disconnect) another user
from the network.


``network/linking``
~~~~~~~~~~~~~~~~~~~

This permission allows the target to modify linking parameters for the network.
This includes pairing, unpairing, terminating servers, adding new servers, and
other potentially dangerous commands.  This should only be granted to operators
that absolutely requires these abilities.


``network/override``
~~~~~~~~~~~~~~~~~~~~

This is a nested permission that allows a network operator to override certain
restrictions.  The following sub-permissions are available:

:acl: The target can change ACLs for groups they do not have a regular
      permission on, or for users other than themself.
:ban: The target can join a group even if they are banned.
:property: The target can set properties on groups they do not own.
:\*: Grants the target *all* override permissions.


``network/rewrite_history``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This permission allows the target to change timestamps for critical network
metadata.  This permission should only be used in the limited case of restoring
information from a backup.



Alternative authentication methods
----------------------------------

Most users of GlorIRCd will sign on to their network using an account name and
passphrase.  However, there are other methods available that can potentially
provide better security than just a passphrase.


Client Certificates
```````````````````

You can use a **client certificate** to authenticate to GlorIRCd.  This involves
obtaining a **private key** that only you have.  You must keep the key file a
closely-guarded secret, and use a strong passphrase on it.  However, the
passphrase is only used on your own computer to unlock the key file, which is
then used to authenticate you to GlorIRCd.  This adds a layer of protection as
the server itself has no record of your passphrase, keeping you safe from a
network breach.

To use a client certificate, blah blah blah CERTFP blah blah blah SHA-256 ONLY
blah blah blah TLS REQUIRED blah blah blah GET A GOOD WARNING ABOUT THE DANGERS
OF CLIENT CERTS FROM ELLY, HORST, OR GRAWITY.


2fa
```

XXX do we want to hook into Authy?  It would be pretty easy and give us 2fa for
virtually no effort using their Python API.


Kerberos
````````

If your network administrator has enabled Kerberos authentication, you may use
a Kerberos ticket to authenticate to GlorIRCd.



TLS 1.2 and You
---------------

.. note:: This is not meant to be an exhaustive resource about TLS.  We just
          want to contribute to the further education of our glorious users. :)

**TLS**, or **Transport Layer Security**, is a protocol allowing secure
communication across a computer network.  Most communication across a network
occurs in plain-text, and anyone on the same network as you can freely read any
data sent in this way.  In the case of the Internet, this is a very large number
of people.  TLS provides added security by encrypting the data before it leaves
your computer, and decrypting it only when it arrives at the destination.

TLS cannot provide a 100% guarantee of security, and you must still be cautious
with your authentication information and your private data.  However, modern TLS
such as that used by GlorIRCd can add a reliable layer of security.

GlorIRCd, by default, requires TLS version 1.2 to connect.  This is a relatively
new version of TLS and not all computers support it yet.  If you see a security
related error when you try to connect to an IRC network - whether it runs
GlorIRCd or otherwise - you should first make sure you are running the latest
software available for your computer.  There are many ways to do this depending
on your system, and this guide can't possibly hope to cover them all, but if you
aren't sure how to do that for your computer, consult your online help or ask a
knowledgeable friend for help.  Microsoft Windows users can visit the Security
Centre at microsoft.com/security.  Apple users can go to their local Genius Bar.
Linux users should refer to their distribution's documentation or Web site (try
ubuntu.com or debian.org if you aren't sure).

TLS version 1.2 is currently the most secure protocol available for production
Internet servers, and can take advantage of many recent advances in security.
It is very important to use this new protocol as the older protocol versions are
weaker, and some are even vulnerable to malicious users.

Here are some common questions, and answers to them.


Why does my computer say "invalid certificate" when I connect to a network?
```````````````````````````````````````````````````````````````````````````

The network may not have a certificate signed by a trusted Certification
Authority, which are companies that provide verification that the registrant of
a certificate is who they say they are, and not an imposter.  If you see a
message about "self signed" certificates, this is almost certainly the case.
There are two main courses of action to remain fully safe:

* Email the administrators of that network, asking them to obtain a legitimate
  certificate.  There are projects such as Lets Encrypt and StartSSL that allow
  them to obtain these free of charge.

* Don't connect to that network.

If you are sure the network has a valid certificate that has been signed by a
trusted authority, your computer may have an issue with its "Trust Store".  You
can search online for ways to resolve this problem based on what system you are
using (Windows, OS X, Linux).


What does "protocol mismatch" (or "client version invalid") mean?
`````````````````````````````````````````````````````````````````

Your computer is not able to communicate using the TLS version 1.2 protocol.
You should update your computer as described above.


Where can I learn about security and TLS?
`````````````````````````````````````````

* A very good resource for beginners that talks in plain terms without resorting
  to sounding condescending can be found at:
  http://jordanfried.com/beginners-guide-to-internet-security/

* A more in-depth resource for people who want to be safe online and want to do
  more research can be found at: http://www.grassrootsdesign.com/intro/security



Best practices for users
------------------------

This section outlines some Good Ideas™ for users of GlorIRCd to stay secure.


Don't share your passphrase
```````````````````````````

Your passphrase is yours, and yours alone.  A network operator will never need
your passphrase; they can look at any relevant information about you without it.
If someone asks for your passphrase, you should notify an operator immediately.




Operator security
=================

This chapter describes operator-facing security features of GlorIRCd, and all
relevant configuration options you can use to ensure your network is as safe as
possible.



Configuration
-------------

This section describes the most important configuration options that affect the
security of GlorIRCd.  This list is not exhaustive, and other options may
additionally affect the security of your network.  Common sense goes a long way.


ssl_ciphers
```````````

This option is found in your chosen I/O module backend, if it supports SSL/TLS.
The default is based on the Modern TLS Server settings recommended by the
`Mozilla Foundation`_.  You should not change this setting without a good
understanding of how the underlying TLS protocol (and OpenSSL) chooses ciphers.

.. warning:: Changing this value can render connections to your server unusable!
             Use care when changing this value.

.. _`Mozilla Foundation`:
   https://wiki.mozilla.org/Security/Server_Side_TLS#Modern_compatibility


passphrase_min_chars
````````````````````

This option is found in the Data Store section of your configuration.  It is
strongly encouraged to set this to at least 8.

.. warning:: Setting this to a lower value can severely compromise the security
             of your network.


The ``network/inject`` permission
`````````````````````````````````

This permission allows the target to inject any command in to the network with
the same privilege as the server to which the target is connected.  This has
very severe security (and stability) ramifications, and should never be used.
As it is equivalent to "OperServ RAW" on traditional IRC networks, it sets an
internal "tainted" flag when this permission is active on the network.


A note on TLS v1.2
``````````````````

While there is no configuration option to allow lower TLS versions (on purpose),
as GlorIRCd is open source, it is possible to modify the source directly to
allow older clients to connect.  Please do not do this.  There are multiple
vulnerabilities in older versions of SSL and TLS.  Instead, encourage your users
to upgrade their software to keep themselves - and you - safer.
