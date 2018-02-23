from .tokens import TOKEN_COMMAND_TAB_NEXT
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('tabnext', 'tabn')
class TokenCommandTabNext(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__([], TOKEN_COMMAND_TAB_NEXT, 'tabnext', *args, **kwargs)
        self.target_command = 'ex_tabnext'


def scan_cmd_tab_next(state):
    c = state.consume()
    if c == state.EOF:
        return None, [TokenCommandTabNext(), TokenEof()]

    bang = c == '!'

    return None, [TokenCommandTabNext(forced=bang), TokenEof()]
