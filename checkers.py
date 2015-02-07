import base64

from twisted.conch import error
from twisted.conch.ssh import keys
from twisted.cred import checkers, credentials
from twisted.python import failure, log
from zope.interface import implementer


@implementer(checkers.ICredentialsChecker)
class PublicKeyCreditentialsChecker:
    credentialInterfaces = (credentials.ISSHPrivateKey,)

    def __init__(self, authorized_keys):
        self.authorizedKeys = authorized_keys

    def requestAvatarId(self, credentials):
        log.msg(credentials)
        user_key_string = self.authorizedKeys.get(credentials.username)
        if not user_key_string:
            return failure.Failure(error.ConchError('No such user'))

        # strip ssh-rsa type before decoding
        decoded_string = base64.decodestring(user_key_string.split(' ')[1])
        if decoded_string != credentials.blob:
            raise failure.Failure(error.ConchError('I don\'t recognize this key'))

        if not credentials.signature:
            raise error.ValidPublicKey()

        user_key = keys.Key.fromString(data=user_key_string)
        if user_key.verify(credentials.signature, credentials.sigData):
            return credentials.username
        else:
            log.err('Signature check failed!')
            return failure.Failure(error.ConchError('Incorrect signature'))
