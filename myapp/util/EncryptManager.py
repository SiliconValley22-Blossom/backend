import hashlib


def encrypt(rowPassword):
    m = hashlib.sha256()
    m.update(rowPassword.encode('utf-8'))

    return m.hexdigest()[:30]


def checkPassword(encryptPassword, rowPassword):
    m = hashlib.sha256()
    m.update(rowPassword.encode('utf-8'))

    toEncrypt = m.hexdigest()[:30]

    return encryptPassword == toEncrypt
