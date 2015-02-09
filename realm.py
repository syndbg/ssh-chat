from twisted.conch.avatar import ConchUser
from twisted.conch.insults import insults
from twisted.conch.interfaces import IConchUser, ISession
from twisted.conch.ssh import session
from twisted.cred.portal import IRealm
from twisted.python import log
from zope.interface import implementer

from protocol import ChatProtocol


@implementer(ISession)
class ChatAvatar(ConchUser):

    def __init__(self, username):
        ConchUser.__init__(self)
        self.username = username
        self.channelLookup.update({'session': session.SSHSession})

    def openShell(self, protocol):
        server_protocol = insults.ServerProtocol(ChatProtocol, self)
        server_protocol.makeConnection(protocol)
        protocol.makeConnection(session.wrapProtocol(server_protocol))

    def getPty(self, terminal, window_size, attrs):
        return None

    def execCommand(self, protocol, cmd):
        raise NotImplementedError

    def closed(self):
        log.msg('{0} session got closed'.format(self.username))


@implementer(IRealm)
class ChatRealm:

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IConchUser not in interfaces:
            raise NotImplementedError('No supported interfaces found.')
        return interfaces[0], ChatAvatar(avatarId), lambda: None
