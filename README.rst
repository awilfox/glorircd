==================
 GlorIRCd charter
==================
:Authors:
  * **Andrew Wilcox**
:Version:
  1.0
:Status:
  Draft
:Copyright:
  © 2015 Andrew Wilcox.  NCSA open source licence.



Requirements
============

Background
----------
The current IRC daemons available for production use today are lacking in many
areas: features, compatibility, reliability.  A new, modern IRC daemon is not
only desired, but needed.


Opportunity
-----------
As the IRCv3 protocol moves forward on standards track[1], having an easily
extensible server will allow us to capture more market share.  Implementing
new features of the protocol first will be a defining trait.  It will also
enable the protocol details to be hashed out and made better, making a lasting
impact on the larger Internet community.

[1]: http://irvc3.net/


Objectives / success critera
----------------------------
* Implement the entire IRCv3 protocol.
* Be production-quality by Q4 2015.




Solution vision
===============

Vision statement
----------------
For peer-to-peer chat systems, GlorIRCd is an IRC daemon that will scale well,
be fault tolerant, and compliant with bleeding-edge standards.  Unlike other IRC
daemons, GlorIRCd is designed to be easy to extend and maintain.  GlorIRCd is
also designed to be highly fault tolerant for mission-critical chat systems.
It is also designed to operate stand-alone, without an extra "services" package.


Major features
--------------
#. Modular core allowing for new features to be written and tested easily, and
   allowing for on-the-fly patching for high availability.

#. Standards-compliance with IRCv3.

#. Fault tolerance via a different form of server linking.

#. Nickname and channel registration is handled inside the daemon.




Project Scope and Limitations
=============================

Scope of initial release (v1)
-----------------------------
The initial release will focus on the core and linking protocol.  Therefore the
initial release may not be immediately production-ready.  It will be a testbed
for ideas and innovations in the IRC ecosystem.


Scope of next release (v2)
--------------------------
The second release will focus on extremely high availability and production
scenarios.


Scope of future releases
------------------------
Continued evolution in the design and linking protocol are anticipated.
Additionally, more IRCv3 extensions will likely be introduced.


Limitations and exclusions
--------------------------
Linking to other IRC daemons is not a goal.
