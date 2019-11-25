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


def checkLogIn(logInCommand):
    if not (logInCommand == "1" or logInCommand == "2"):
        raise ValueError("Something other than 1 or 2 was entered")


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


def main():
    while True:
        showLogInMenu()
        logInCommand = input()
        try:
            checkLogIn(logInCommand)
        except ValueError:
            print("\nErreur: Veuillez entrer 1 ou 2\n")
        else:
            break

    if logInCommand == "1":
        createAccount()
    else:
        logIn()


if __name__ == "__main__":
    main()
