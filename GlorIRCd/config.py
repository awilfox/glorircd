# -*- coding: utf-8 -*-
# Copyright © 2015 by the GlorIRCd team.  All rights reserved.
# See COPYING file included with this source for more information.

"""Defines the core configuration primitives for GlorIRCd.

Note that as the configuration has to be loaded before the module system can
initialise, this is the only area of GlorIRCd that can never be modularised.
So we have to detect configuration format changes on every configuration reload.
This kind of sucks.
"""

