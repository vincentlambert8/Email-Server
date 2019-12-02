#!/usr/bin/python2.4
# -*- coding: utf-8 -*-
import socket

import util
import optparse
import sys


def getparserArgument():
    parser = optparse.OptionParser()
    parser.add_option("-p", "--port", dest="port", type=int, default=1400,
                        help="port sur lequel envoyer et écouter les messages")
    return parser.parse_args(sys.argv[1:])[0]


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
    data = {"command": "signup", "username": username, "password": password}
    message = str(data)

    sendMessageToServer(message)


def logIn():
    username, password = getAccountCredentials()
    data = {"command": "login", "username": username, "password": password}
    message = str(data)

    sendMessageToServer(message)


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
            print("La commande entrée est invalide. Veuillez entrer un nombre de 1 à 2")

    return logInCommand


def getMainMenuCommand():
    successfulCommand = False
    while not successfulCommand:
        showMainMenu()
        mainMenuCommand = input()
        successfulCommand = checkMainMenuCommand(mainMenuCommand)
        if not successfulCommand:
            print("La commande entrée est invalide. Veuillez entrer un nombre de 1 à 4")

    return mainMenuCommand


def createSocket():
    port = getparserArgument().port
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(("localhost", port))
    return clientSocket


def sendMessageToServer(message):
    #CLIENT_SOCKET.send(bytes(message, encoding="utf-8"))
    CLIENT_SOCKET.send(message.encode())


def receiveMessageFromServer(clientSocket):
    data = clientSocket.recv(512)
    return data


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
    CLIENT_SOCKET = createSocket()
    main()
