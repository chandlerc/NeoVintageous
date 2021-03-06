# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

import builtins
import logging
import os
import re

import sublime

from NeoVintageous.nv.vim import message


_log = logging.getLogger(__name__)


# A specific list of ex commands are supported.
# NOTE: The recursive mapping commands `:map`, `:nmap`, `:omap`, `:smap`,
# `:vmap` are not supported. They were removed in v1.5. They are included in the
# parse pattern because a notice is emitted if they are used. Uses should use
# the non recursive commands instead. The recursive mappings were because they
# were not implemented as recursive mappings, and replacing them now may prevent
# some potential problems in the future if the recursive commands are ever
# implemented.
_parse_line_pattern = re.compile(
    '^(?::)?(?P<cmdline>(?P<cmd>noremap|map|nnoremap|nmap|snoremap|smap|vnoremap|vmap|onoremap|omap|let) .*)$')


_recursive_mapping_alts = {
    'map': 'nnnoremap',
    'nmap': 'nnoremap',
    'smap': 'snoremap',
    'vmap': 'vnoremap',
    'omap': 'onoremap'
}


def _file_name():
    # TODO v2.0.0 Rename .vintageousrc file -> .neovintageousrc
    return os.path.join(sublime.packages_path(), 'User', '.vintageousrc')


def open(window):
    file = _file_name()

    if not os.path.exists(file):
        with builtins.open(file, 'w') as f:
            f.write('" Type :h vintageousrc for help.\n')

    window.open_file(file)


def load():
    _run()


def reload():
    _run()


def _run():
    _log.debug('run %s', _file_name())

    from NeoVintageous.nv.ex_cmds import do_ex_cmdline

    try:
        window = sublime.active_window()
        with builtins.open(_file_name(), 'r') as f:
            for line in f:
                cmdline = _parse_line(line)
                if cmdline:
                    # TODO [review] Should do_ex_cmdline() make the colon optional?
                    do_ex_cmdline(window, ':' + cmdline)

    except FileNotFoundError:
        _log.debug('rcfile not found')


def _parse_line(line):
    try:
        line = line.rstrip()
        if line:
            match = _parse_line_pattern.match(line)
            if match:
                cmd = match.group('cmd')
                if cmd in _recursive_mapping_alts:
                    raise Exception('Recursive mapping commands are not allowed, use the "{}" command instead'
                                    .format(_recursive_mapping_alts[cmd]))

                cmdline = match.group('cmdline')

                # By default, mapping the character '|' (bar) should be escaped
                # with a slash or '<Bar>' used instead. Neovintageous currently
                # doesn't support '<Bar>' and internally doesn't require the bar
                # character to be escaped, but in order not to break backwards
                # compatibility in the future, this piece of code checks that
                # the mapping escapes the bar character correctly. This piece of
                # code can be removed when this is fixed in the core. See :help
                # map_bar for more details.
                if '|' in cmdline:
                    if '|' in cmdline.replace('\\|', ''):
                        raise Exception('E488: Trailing characters: {}'.format(line.rstrip()))

                    cmdline = cmdline.replace('\\|', '|')

                return cmdline
    except Exception:
        # TODO [review] Exception handling
        msg = 'error detected while processing {} at line {}'.format(_file_name(), line.rstrip())
        message(msg)
        _log.debug(msg)

    return None
