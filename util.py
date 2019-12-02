import getpass
from hashlib import sha256
from os import path, mkdir
from re import search


def searchString(regex, string):
    return search(regex, string)


def hashPassword(password):
    return sha256(password.encode()).hexdigest()


def inputPassword():
    return getpass.getpass("Mot de passe: ")


def checkIfFileExists(filePath):
    return path.exists(filePath)


def createDirectory(name):
    mkdir(name)
    print("made dir")
