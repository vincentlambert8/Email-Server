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


def logIn(username, password):
    filePath = f"{username}/config.txt"
    if util.checkIfFileExists(filePath):
        pass
    print("Le nom d'utilisateur entré n'existe pas. Veuillez recommencer")


def usernameIsValid(username):
    path = f"{username}/config.txt"
    return not util.checkIfFileExists(path)


def passwordIsValid(password):
    regex = "^(?=.*[a-z])(?=.*[A-Z])(?=(.*?\d){2})[a-zA-Z\d]{6,12}$"
    return util.searchString(regex, password)
