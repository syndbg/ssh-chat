from os.path import expanduser

from twisted.conch.ssh import keys


def get_key(path):
    with open(path) as f:
        contents = f.read()
    return keys.Key.fromString(data=contents)


def get_RSA_keys():
    ssh_folder = expanduser('~/.ssh/')
    public_key = get_key(ssh_folder + 'id_rsa.pub')
    private_key = get_key(ssh_folder + 'id_rsa')
    return public_key, private_key
