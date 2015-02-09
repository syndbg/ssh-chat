import sys

from twisted.internet import reactor
from twisted.cred import portal
from twisted.python import log

from protocol import ChatProtocolFactory
from checkers import PublicKeyCreditentialsChecker, AllowAnnomyousKeysChecker
from realm import ChatRealm
from helpers import get_RSA_keys


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    factory = ChatProtocolFactory()
    realm = ChatRealm()
    factory.portal = portal.Portal(realm)

    checker = AllowAnnomyousKeysChecker()
    factory.portal.registerChecker(checker)

    public_key, private_key = get_RSA_keys()
    factory.publicKeys = {'ssh-rsa': public_key}
    factory.privateKeys = {'ssh-rsa': private_key}

    reactor.listenTCP(2222, factory)
    reactor.run()
