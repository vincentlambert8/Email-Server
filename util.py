import getpass
from hashlib import sha256
from os import path, mkdir


def hashPassword(password):
    return sha256(password.encode()).hexdigest()


def inputPassword():
    return getpass.getpass("Mot de passe: ")


def checkIfFileExists(filePath):
    return path.exists(filePath)


def createDirectory(name):
    mkdir(name)
