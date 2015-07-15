# -*- coding: utf-8 -*-
"""
Creation of the prompt used by terminal interface.
Call create_prompt(0) function for receive a callable that manage the user prompt.

parse(1) function take the callable in parameter and returns
the user request ready to be treated.

"""


#########################
# IMPORTS               #
#########################
from prompt_toolkit.contrib.completers                   import WordCompleter
from prompt_toolkit.contrib.regular_languages.compiler   import compile as pt_compile
from prompt_toolkit.contrib.regular_languages.completion import GrammarCompleter
from prompt_toolkit.contrib.regular_languages.lexer      import GrammarLexer
from prompt_toolkit.shortcuts                            import get_input
from prompt_toolkit.styles                               import DefaultStyle
from pygments.token                                      import Token
from collections                                         import defaultdict, ChainMap
import tia.commons as commons
import tia.agents
import itertools
import functools
import math

LOGGER = commons.logger()

# some precomputed values
AGENT_CLASS = {
    n.lower(): c
    for n, c in tia.agents.__dict__.items()
    if callable(c) and issubclass(c, tia.agents.Agent)
    and c is not tia.agents.Agent
}
AGENTS_NAME = tuple(AGENT_CLASS.keys())
# lexems tokens for pygments
TOKENS = {
    'cmd'    : Token.Command,
    'subcmd' : Token.Operator,
    'args'   : Token.Other,
}

# commands regex and aliases
COMMANDS = {
    'request': ('request', 'r', 'req'),
    'lists'  : ('ls', 'l', 'lists', 'listing'),
    'help'   : ('help', 'h'),
    'quit'   : ('quit', 'q', 'exit'),
}
SUBCOMMANDS = {
    'agent'  : AGENTS_NAME,
    'player' : ('players', 'player'),
}
ARGUMENTS = {
    'args'   : (r'.*',),
    'coords' : (r'[0-9]+\s[0-9]+',),
}
# link between level name and dict
LEVELS = {
    'cmd'    : COMMANDS,
    'subcmd' : SUBCOMMANDS,
    'args'   : ARGUMENTS,
}
# reverse dicts
unalias_level = lambda d: {alias:k for k, aliases in d.items() for alias in aliases}
COMMANDS_UNALIAS = unalias_level(COMMANDS)
SUBCOMMANDS_UNALIAS = unalias_level(SUBCOMMANDS)
ARGUMENTS_UNALIAS = unalias_level(ARGUMENTS)
UNALIAS = ChainMap({}, COMMANDS_UNALIAS, SUBCOMMANDS_UNALIAS, ARGUMENTS_UNALIAS)
REV_LEVELS = defaultdict(lambda: 'args', {cmd:level
              for level, cmds in LEVELS.items()
              for cmds in cmds.values()
              for cmd  in cmds
             })
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
    global GRAMMAR_RAW
    GRAMMAR_RAW = (
        cmd2grm('request', 'agent' , 'coords')
        + cmd2grm('lists', 'player',  None   )
        + cmd2grm('lists', 'agent' ,  None   )
        + cmd2grm('help' ,  None   ,  None   )
        + cmd2grm('quit' ,  None   ,  None   )
    )
    LOGGER.debug('GRAMMAR:\n' + GRAMMAR_RAW)
    return pt_compile(GRAMMAR_RAW)
GRAMMAR     = commands_grammar()


class ExampleStyle(DefaultStyle):
   styles = {}
   styles.update(DefaultStyle.styles)
   styles.update({
       Token.Command : 'bg:#662222 #aa3333 bold',
       Token.Operator: 'bg:#662222 #aa3333 bold',
       Token.Other   : 'bg:#662222 #aa3333 bold',
   })




def create_prompt():
    lexer = {
        name : token
        for token, level in ((Token.Command , COMMANDS),
                             (Token.Operator, SUBCOMMANDS),
                             (Token.Other   , ARGUMENTS))
        for names in level.values()
        for name in names
    }
    # print('LEXER:', lexer)
    lexer = GrammarLexer(GRAMMAR, lexer)

    completer = {
        k: WordCompleter(v)
        for item in LEVELS.values()
        for k, v in item.items()
    }
    # print('COMPLETER:', completer)
    completer = GrammarCompleter(
        GRAMMAR,
        completer
    )

    return functools.partial(
        get_input,
        message=DEFAULT_PROMPT,  # text at the beginning
        lexer=lexer, completer=completer,  # cf above
        style=ExampleStyle,  # pygmentation
        patch_stdout=True,  # printings occurs above the prompt line
    )


def parse(prompt):
    """return parsed and formatted user request from prompt
    returned by create_prompt function

    """
    # Read input and parse the result.
    m = GRAMMAR.match(prompt())
    if m is None:
        print('invalid command')
        return None, None, None
    var = defaultdict(lambda: None, {
        REV_LEVELS[alias]: alias
        for _, alias, _ in m.variables().__dict__['_tuples']
    })
    return UNALIAS[var['cmd']], var['subcmd'], var['args']



