class CommandsHandler:

    def __init__(self, protocol):
        self.protocol = protocol
        self.terminal = self.protocol.terminal

    def do_help(self):
        public_methods = [function_name for function_name in dir(
            self) if function_name.startswith('do_')]
        commands = [cmd.replace('do_', '', 1) for cmd in public_methods]
        self.terminal.write('Commands: ' + ' '.join(commands))

    def do_echo(self, *args):
        self.terminal.write(' '.join(args))

    def do_whoami(self):
        self.terminal.write(self.user.username)

    def do_quit(self):
        self.terminal.write('Bye!')
        self.terminal.loseConnection()

    def do_clear(self):
        self.terminal.reset()
