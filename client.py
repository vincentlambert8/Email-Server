#!/usr/bin/python2.4
# -*- coding: utf-8 -*-

import util


def showLogInMenu():
    print("\nMenu de connexion")
    print("1. Créer un compte")
    print("2. Se connecter")


def showMainMenu():
    print("\nMenu principal")
    print("1. Consultation de courriels")
    print("2. Envoi de courriels")
    print("3. Statistiques")
    print("4. Quitter")


def checkLogInCommand(logInCommand):
    return logInCommand == "1" or logInCommand == "2"


def getUsername():
    return input("Nom d'utilisateur: ")


def getPassword():
    return util.inputPassword()


def getAccountCredentials():
    username = getUsername()
    password = getPassword()

    return username, password


def createAccount():
    username, password = getAccountCredentials()

    #TODO trouver comment faire pour envoyer une commande au serveur
    sendCommandToServer(createAccount, username, password)


def logIn():
    username, password = getAccountCredentials()

    #TODO trouver comment faire pour envoyer une commande au serveur
    sendCommandToServer(logIn, username, password)


def checkMainMenuCommand(mainMenuCommand):
    choices = {"1", "2", "3", "4"}
    return mainMenuCommand in choices


def getLoginCommand():
    successfulCommand = False
    while not successfulCommand:
        showLogInMenu()
        logInCommand = input()
        successfulCommand = checkLogInCommand(logInCommand)
        if not successfulCommand:
            print("La commande entrée est invalie. Veuillez entrer un nombre de 1 à 2")

    return logInCommand


def getMainMenuCommand():
    successfulCommand = False
    while not successfulCommand:
        showLogInMenu()
        mainMenuCommand = input()
        successfulCommand = checkMainMenuCommand(logInCommand)
        if not successfulCommand:
            print("La commande entrée est invalie. Veuillez entrer un nombre de 1 à 4")

    return mainMenuCommand


def main():
    logInCommand = getLoginCommand()
    if logInCommand == "1":
        createAccount()
    else:
        logIn()

    mainMenuCommand = getMainMenuCommand()
    if mainMenuCommand == "1":
        checkMails()
    elif mainMenuCommand == "2":
        sendMails()
    elif mainMenuCommand == "3":
        checkStats()
    else:
        quit()


if __name__ == "__main__":
    main()
