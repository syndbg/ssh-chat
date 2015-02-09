from twisted.conch.recvline import HistoricRecvLine
from twisted.conch.client.direct import SSHClientFactory
from twisted.python import log

from commands import CommandsHandler


class ChatProtocol(HistoricRecvLine):

    def __init__(self, user, factory=None):
        self.user = user
        self.username = self.user.username
        self.factory = factory
        self.commands = CommandsHandler(self)

    def connectionMade(self):
        HistoricRecvLine.connectionMade(self)
        log.msg('{0} logged in'.format(self.username))
        self.terminal.write('Welcome! {0}'.format(self.username))
        self.terminal.nextLine()
        self.do_help()
        self.show_prompt()

    def show_prompt(self):
        self.terminal.write('[{0}] '.format(self.username))

    def get_command_function(self, cmd):
        return getattr(self.commands, 'do_' + cmd, None)

    def lineReceived(self, line):
        line = line.strip()
        if line:
            log.msg('[{0}] {1}'.format(self.username, line))
            if line.startswith('/'):
                cmd_and_args = line[1:].split(' ')
                cmd = cmd_and_args[0]
                args = '' if len(cmd_and_args) < 2 else cmd_and_args[1:]
                self.try_execute_command(cmd, args)
            else:
                self.terminal.nextLine()
        self.show_prompt()

    def try_execute_command(self, cmd, args):
        function = self.get_command_function(cmd)
        try:
            function(*args)
            log.msg('Command {0} executed by {1}.'.format(function.func_name, self.username))
        except TypeError:
            log.err('Invalid number of arguments given for {0} by {1}'.format(cmd, self.username))
            self.terminal.write('Invalid numers of arguments given!')
        except Exception as e:
            log.err('Failed to execute command {0} by {1}'.format(cmd, self.username))
            self.terminal.write('Error: {0}'.format(e))
        finally:
            self.terminal.nextLine()


class ChatProtocolFactory(SSHClientFactory):

    def __init__(self):
        self.users = {}

    def buildProtocol(self):
        return ChatProtocol(self)
