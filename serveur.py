#!/usr/bin/python2.4
# -*- coding: utf-8 -*-

import util


def createUserConfigFile(username, password):
    createUserDirectory(username)

    filePath = f"{username}/config.txt"
    with open(filePath, "w") as file:
        hashedPassword = util.hashPassword(password)
        file.write(hashedPassword)


def createUserDirectory(username):
    util.createDirectory(username)


def passwordMatches(password, filePath):
    with open(filePath, "r") as file:
        originalHash = file.readline()
        enteredHash = util.hashPassword(password)
        return originalHash == enteredHash


def logIn(username, password):
    while not tryToLogIn(username, password):
        continue
    # TODO Trouver comment communiquer avec le client
    sendCommandToClient(showOptionMenu)


def tryToLogIn(username, password):
    filePath = f"{username}/config.txt"
    if not util.checkIfFileExists(filePath):
        print("Le nom d'utilisateur entré n'existe pas. Veuillez recommencer")
        return False
    if not passwordMatches(password, filePath):
        print("Le mot de passe entré est invalide. Veuillez recommencer")
        return False
    return True


def usernameIsValid(username):
    path = f"{username}/config.txt"
    return not util.checkIfFileExists(path)


def passwordIsValid(password):
    regex = "^(?=.*[a-z])(?=.*[A-Z])(?=(.*?\d){2})[a-zA-Z\d]{6,12}$"
    return util.searchString(regex, password)
