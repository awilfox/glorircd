# -*- coding: utf-8 -*-
# Copyright © 2015 by the GlorIRCd team.  All rights reserved.
# See COPYING file included with this source for more information.

"""Defines the core configuration primitives for GlorIRCd.

Note that as the configuration has to be loaded before the module system can
initialise, this is the only area of GlorIRCd that can never be modularised.
So we have to detect configuration format changes on every configuration reload.
This kind of sucks.

config_hive.mod_config is a dict of {module name: {key:value}}.
"""


from configparser import ConfigParser
import os
import sys
from taillight.signal import Signal

from GlorIRCd.errors import ConfigError


config_updated = Signal('config/updated')
"""Signal called when the configuration hive is updated/reloaded."""


def find_root():
    """Find the configuration root."""

    def conf_exists_in_dir(dir_):
        return any([os.path.exists(os.path.join(dir_, 'etc', 'glorircd')),
                    os.path.exists(os.path.join(dir_, 'etc', 'glorircd.conf'))])

    # ugly.
    parent_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

    if conf_exists_in_dir(parent_dir):
        return parent_dir

    home_dir = os.path.expanduser('~')
    if conf_exists_in_dir(home_dir):
        return home_dir

    prefix = sys.prefix
    if prefix == '/usr':
        prefix = '/'

    if conf_exists_in_dir(prefix):
        return prefix

    searched = ", ".join((parent_dir, home_dir, prefix))
    raise ConfigError("No configuration file (searched {}).".format(searched))


class ConfigurationHive:
    def __init__(self, search_paths=['/etc/glorircd', '/etc'], root=find_root):
        """Initialise the GlorIRCd configuration hive.

        :param list search_paths:
            An iterable containing the paths to search for glorircd.conf inside
            the specified root.  Defaults to /etc/glorircd and /etc.

        :param callable root:
            A callable that will determine the appropriate root to search under.
            The default callable is roughly equivalent to:

            .. code-block ::
                def find_root():
                    if 'etc/glorircd*' in parent_directory_of_GlorIRCd:
                        return parent_directory_of_GlorIRCd
                    elif 'etc/glorircd*' in home_directory_of_user:
                        return home_directory_of_user
                    else:
                        return sys.prefix

        :effects:
            The configuration hive is loaded.
        """

        config_path = root()
        glorircd_dir = os.path.join(config_path, 'etc', 'glorircd')
        if os.path.exists(glorircd_dir):
            self.path = glorircd_dir
            self._load_config_from(os.path.join(glorircd_dir, 'glorircd.conf'))
        else:
            self.path = os.path.join(config_path, 'etc')
            self._load_config_from(os.path.join(self.path, 'glorircd.conf'))

    def __repr__(self):
        return "ConfigurationHive(loaded_from={})".format(self.loaded_from)

    def _load_config_from(self, file_path):
        """Load the configuration from a file (ConfigParser syntax).

        :param str file_path:
            The path to the configuration file.

        :effects:
            The configuration hive is loaded from the specified file.

        :raises FileNotFoundError:
            If the file specified in file_path does not exist.

        :raises :py:exc:`~GlorIRCd.errors.ConfigError`:
            If an important configuration option is missing or invalid.
        """

        with open(file_path, 'r') as config_file:
            parser = ConfigParser(allow_no_value=True)
            parser.read_file(config_file)
            if not parser.has_section('server'):
                raise ConfigError("Missing required section: server")
            self.server = dict(parser.items('server'))
            self.modules = list(mod[0] for mod in parser.items('modules'))
            self.mod_config = {sect: dict(parser.items(sect))
                               for sect in parser.sections()
                               if sect != 'server' and sect != 'modules'}
            self.loaded_from = file_path
            config_updated.call('master')
