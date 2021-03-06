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

from sublime import status_message as _status_message


# TODO [review] Some of these modes appear unused or not needed
# XXX The modes Use strings because we need to pass modes as arguments in
# Default.sublime-keymap and it's more readable.
COMMAND_LINE = 'mode_command_line'
CTRL_X = 'mode_control_x'
INSERT = 'mode_insert'
# NeoVintageous always runs actions based on selections. Some Vim commands,
# however, behave differently depending on whether the current mode is NORMAL or
# VISUAL. To differentiate NORMAL mode operations (involving only an action, or
# a motion plus an action) from VISUAL mode, we need to add an additional mode
# for handling selections that won't interfere with the actual VISUAL mode.
# This is INTERNAL_NORMAL's job. We consider INTERNAL_NORMAL a pseudomode,
# because global state's .mode property should never set to it, yet it's set in
# vi_cmd_data often.
# Note that for pure motions we still use plain NORMAL mode.
INTERNAL_NORMAL = 'mode_internal_normal'
NORMAL = 'mode_normal'
NORMAL_INSERT = 'mode_normal_insert'  # The mode you enter when giving i a count
OPERATOR_PENDING = 'mode_operator_pending'
REPLACE = 'mode_replace'
SELECT = 'mode_select'
UNKNOWN = 'mode_unknown'
VISUAL = 'mode_visual'
VISUAL_BLOCK = 'mode_visual_block'
VISUAL_LINE = 'mode_visual_line'


_MODE_NAMES = {
    INSERT: 'INSERT',
    INTERNAL_NORMAL: '',
    NORMAL: '',
    OPERATOR_PENDING: '',
    VISUAL: 'VISUAL',
    VISUAL_BLOCK: 'VISUAL BLOCK',
    VISUAL_LINE: 'VISUAL LINE',
    UNKNOWN: 'UNKNOWN',
    REPLACE: 'REPLACE',
    NORMAL_INSERT: 'INSERT',
    SELECT: 'SELECT',
    CTRL_X: 'Mode ^X'
}


def mode_to_name(mode):
    # type: (str) -> str
    try:
        return _MODE_NAMES[mode]
    except KeyError:
        return 'REALLY UNKNOWN'


INPUT_IMMEDIATE = 1
INPUT_VIA_PANEL = 2
INPUT_AFTER_MOTION = 3


DIRECTION_NONE = 0
DIRECTION_UP = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 4


def console_message(msg):
    # type: (str) -> None
    print('NeoVintageous:', msg)


def status_message(msg):
    # type: (str) -> None
    _status_message(msg)


def message(msg):
    # type: (str) -> None
    status_message(msg)
    console_message(msg)
