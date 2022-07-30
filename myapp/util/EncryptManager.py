import hashlib


def encrypt(rawPassword):
    m = hashlib.sha256()
    m.update(rawPassword.encode('utf-8'))

    return m.hexdigest()[:30]


def checkPassword(encryptPassword, rawPassword):
    m = hashlib.sha256()
    m.update(rawPassword.encode('utf-8'))

    toEncrypt = m.hexdigest()[:30]

    return encryptPassword == toEncrypt
