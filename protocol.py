from twisted.conch.recvline import HistoricRecvLine
from twisted.conch.client.direct import SSHClientFactory
from twisted.python import log


class ChatProtocol(HistoricRecvLine):

    def __init__(self, factory, user):
        self.factory = factory
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
            log.msg(line)
            cmd_and_args = line.split()
            cmd = cmd_and_args[0]
            args = cmd_and_args[1:]
            function = self.get_command_function(cmd)
            if function:
                try:
                    function(*args)
                    log.msg('{0} executed command {1}.'.format(self.username, function.func_name))
                except Exception as e:
                    log.err('{0} failed to execute command {1}.'.format(self.username, function.func_name))
                    self.terminal.write('Error: {0}'.format(e))
                    self.terminal.nextLine()
            else:
                log.err('{0} tried to execute a non-existing command.')
                self.terminal.write('No such command.')
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
