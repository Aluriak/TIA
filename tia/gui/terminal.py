# -*- coding: utf-8 -*-
"""
Terminal interface for the game.
Substitute for the future Qt interface.

"""


#########################
# IMPORTS               #
#########################
# from tia.info        import PACKAGE_NAME
# from tia.mixins      import Placable
# from tia.coords      import Coords
# from tia.commands    import MoveCommand, QuitCommand
# from tia.agents      import Squad
# from pyglet.window   import key
# from pyglet.window   import mouse
# import itertools
# import functools
# import pyglet
# import types

from prompt_toolkit.contrib.completers                   import WordCompleter
from prompt_toolkit.contrib.regular_languages.compiler   import compile as pt_compile
from prompt_toolkit.contrib.regular_languages.completion import GrammarCompleter
from prompt_toolkit.contrib.regular_languages.lexer      import GrammarLexer
from prompt_toolkit.shortcuts                            import get_input
from prompt_toolkit.styles                               import DefaultStyle
from pygments.token                                      import Token
import tia.commons as commons
import tia.agents
import itertools
import math

LOGGER = commons.logger()

# some precomputed values
AGENTS_NAME = tuple(
    n.lower() for n, c in tia.agents.__dict__.items()
    if callable(c) and issubclass(c, tia.agents.Agent)
)
# commands, subcommmands and arguments
# COMMAND_REQUEST = ('request', 'r', 'req')
# COMMAND_HELP    = ('help', 'h')
# COMMAND_QUIT    = ('quit', 'q', 'exit')
# SUBCOMMAND_AGENT= AGENTS_NAME
# ARGUMENT_ALL    = (r'.*',)
# ARGUMENT_COORDS = (r'[0-9]+[,; ][0-9]+',)

# # aggregations
# COMMANDS    = COMMAND_REQUEST + COMMAND_HELP + COMMAND_QUIT
# SUBCOMMANDS = SUBCOMMAND_AGENT
# ARGUMENTS   = ARGUMENT_ALL + ARGUMENT_COORDS

# # link between level name and aggregations
# LEVELS = {
    # 'cmd'    : COMMANDS,
    # 'subcmd' : SUBCOMMANDS,
    # 'args'   : ARGUMENTS,
# }
TOKENS = {
    'cmd'    : Token.Command,
    'subcmd' : Token.Operator,
    'args'   : Token.Other,
}

# (sub)commands regex and aliases
COMMANDS = {
    'request': ('request', 'r', 'req'),
    'help'   : ('help', 'h'),
    'quit'   : ('quit', 'q', 'exit'),
}
COMMANDS_REV = {v:k for k, v in COMMANDS.items()}
SUBCOMMANDS = {
    'agent'  : AGENTS_NAME,
}
ARGUMENTS = {
    'args'   : (r'.*',),
    'coords' : (r'[0-9]+[,; ][0-9]+',),
}
# link between level name and dict
LEVELS = {
    'cmd'    : COMMANDS,
    'subcmd' : SUBCOMMANDS,
    'args'   : ARGUMENTS,
}
# printings values
DEFAULT_INTRO = 'Type help or ? to list commands.\n'
DEFAULT_PROMPT = '?>'
# COMMANDS
def commands_grammar():
    """Return a grammar for COMMAND_NAMES values."""
    def cmd2grm(cmd, subcmd=None, args=None):
        """layout automatization"""
        return (
            '(\s* (?P<'+cmd+'>(' + '|'.join(COMMANDS[cmd]) + '))'
            + ('' if subcmd is None
               else ('\s+ (?P<'+subcmd+'>(' + '|'.join(SUBCOMMANDS[subcmd]) + ')) \s* '))
            + ('' if args is None
               else ('\s+ (?P<'+args+'>('   + '|'.join(ARGUMENTS[args  ])   + ')) \s* '))
            + ') |\n'
        )
    # get grammar, log it and return it
    grammar = (
        cmd2grm('request', 'agent' , 'coords')
        + cmd2grm('help' ,  None   ,  None   )
        + cmd2grm('quit' ,  None   ,  None   )
    )
    LOGGER.debug('GRAMMAR:\n' + grammar)
    return pt_compile(grammar)


class ExampleStyle(DefaultStyle):
   styles = {}
   styles.update(DefaultStyle.styles)
   styles.update({
       Token.Command : 'bg:#662222 #aa3333 bold',
       Token.Operator: 'bg:#662222 #aa3333 bold',
       Token.Other   : 'bg:#662222 #aa3333 bold',
   })


def test():
    grammar = commands_grammar()

    lexer = {
        name : token
        for token, level in ((Token.Command , COMMANDS),
                             (Token.Operator, SUBCOMMANDS),
                             (Token.Other   , ARGUMENTS))
        for names in level.values()
        for name in names
    }
    print('LEXER:', lexer)
    lexer = GrammarLexer(grammar, lexer)

    completer = {
        k: WordCompleter(v)
        for item in LEVELS.values()
        for k, v in item.items()
    }
    print('COMPLETER:', completer)
    completer = GrammarCompleter(
        grammar,
        completer
    )

    try:
        # REPL loop.
        while True:
            # Read input and parse the result.
            text = get_input(DEFAULT_PROMPT, lexer=lexer,
                             completer=completer, style=ExampleStyle)
            m = grammar.match(text)
            if m is None:
                print('invalid command')
                continue
            var = m.variables()
            print(var.__dict__)
            print(var.get('request'))
            if 'request' in var:
                assert('agent' in var)
                assert('coords' in var)
            else:
                print(var)
    except EOFError:
        pass





class ManagementInterface:
    """
    """


    def __init__(self, player):
        self.player = player
        pass





