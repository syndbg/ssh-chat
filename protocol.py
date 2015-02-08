from twisted.conch.recvline import HistoricRecvLine
from twisted.conch.client.direct import SSHClientFactory
from twisted.python import log


class ChatProtocol(HistoricRecvLine):

    def __init__(self, user):
        # self.factory = factory
        self.user = user
        self.username = self.user.username

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
        return getattr(self, 'do_' + cmd, None)

    def lineReceived(self, line):
        line = line.strip()
        if line:
            log.msg('[{0}] {1}'.format(self.username, line))
            if line.startswith('/'):
                cmd_and_args = line[1:].split(' ')
                cmd = cmd_and_args[0]
                args = '' if len(cmd_and_args) < 2 else cmd_and_args[1:]
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
            else:
                self.terminal.nextLine()
        self.show_prompt()

    def do_help(self):
        public_methods = [function_name for function_name in dir(self) if function_name.startswith('do_')]
        commands = [cmd.replace('do_', '', 1) for cmd in public_methods]
        self.terminal.write('Commands: ' + ' '.join(commands))
        self.terminal.nextLine()

    def do_echo(self, *args):
        self.terminal.write(' '.join(args))
        self.terminal.nextLine()

    def do_whoami(self):
        self.terminal.write(self.user.username)
        self.terminal.nextLine()

    def do_quit(self):
        self.terminal.write('Bye!')
        self.terminal.nextLine()
        self.terminal.loseConnection()

    def do_clear(self):
        self.terminal.reset()


class ChatProtocolFactory(SSHClientFactory):

    def __init__(self):
        self.users = {}

    def buildProtocol(self):
        return ChatProtocol(self)
