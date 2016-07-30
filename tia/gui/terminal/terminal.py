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
from tia.coords       import Coords
from tia.commands     import QuitCommand, AddAgentCommand
from tia.gui.terminal import prompt
import tia.commons as commons
import itertools


class TerminalManagementInterface:
    """
    """


    def __init__(self, engine, player):
        self.engine = engine
        self.player = player
        self.prompt = prompt.create_prompt()
        self.terminated = False


    def run(self):
        """Start the terminal gui: take input, and push commands to the engine

        """
        try:
            while not self.terminated:
                cmd, subcmd, args = prompt.parse(self.prompt)
                if cmd is None:
                    continue
                assert(cmd in self.__class__.__dict__)
                self.__class__.__dict__[cmd](self, subcmd, args)
                self.terminated |= self.engine.terminated
        except EOFError:
            pass
        except KeyboardInterrupt:
            pass
        # send quit command to engine if user ask the prompt to finish
        if not self.terminated:
            self.quit()



    def request(self, subcmd, args):
        """perform a request for a new unit"""
        agent, coords = subcmd, Coords(args.split(' '))
        self.engine.add_command(AddAgentCommand(
            prompt.AGENT_CLASS[agent](coords)
        ))


    def quit(self, subcmd=None, args=None):
        """quit the game"""
        assert(subcmd is None and args is None)
        self.engine.add_command(QuitCommand())
        self.terminated = True


    def lists(self, subcmd, args=None):
        """give list of players or agents"""
        if subcmd == 'players':
            subjects = self.engine.players
        else:
            subjects = self.engine.agents
        print('\n'.join(str(_) for _ in subjects))


    def help(self, subcmd=None, args=None):
        """print the help"""
        print('Grammar:\n', prompt.GRAMMAR_RAW, '\n', sep='')
        for cmd in prompt.LEVELS['cmd']:
            print(cmd.ljust(20), self.__class__.__dict__[cmd].__doc__)
