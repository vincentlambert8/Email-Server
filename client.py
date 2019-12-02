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


def getpassword():
    return util.inputpassword()


def getAccountCredentials():
    username = getUsername()
    password = getpassword()

    return username, password


def createAccount():
    accountSuccessful = False
    while not accountSuccessful:
        username, password = getAccountCredentials()
        data = {"command": "signup", "username": username, "password": password}
        message = str(data)

        sendMessageToServer(message)

        serverResponse = receiveMessageFromServer(CLIENT_SOCKET)
        if serverResponse == "Le nom d'utilisateur est déjà utilisé. Veuillez réessayer.":
            print(serverResponse)
            continue
        elif serverResponse == "Le mot de passe est incorrect. Veuillez réessayer.":
            print(serverResponse)
            continue
        else:
            accountSuccessful = True


def logIn():
    logInSuccessful = False
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


def receiveMessageFromServer():
    data = CLIENT_SOCKET.recv(1024).decode()
    return data


def main():
    connectionMenuSuccess = False
    while not connectionMenuSuccess:
        connectionMenu = receiveMessageFromServer()
        print(connectionMenu)
        logInCommand = input()
        sendMessageToServer(logInCommand)

        serverResponse = receiveMessageFromServer()
        if serverResponse == "La commande entrée est invalide. Veuillez entrer un nombre de 1 à 2":
            print(serverResponse)

        elif serverResponse == "Command successful":
            connectionMenuSuccess = True

    if logInCommand == "1":
        validUsername = False
        while not validUsername:
            serverAskUsername = receiveMessageFromServer()
            print(serverAskUsername)
            username = input()
            sendMessageToServer(username)
            serverResponse = receiveMessageFromServer()
            if serverResponse == "Le nom d'utilisateur est déjà utilisé. Veuillez réessayer.":
                print(serverResponse)

            elif serverResponse == "Username valid":
                validUsername = True

        validPassword = False
        while not validPassword:
            password = util.inputpassword()
            sendMessageToServer(password)

            serverResponse = receiveMessageFromServer()
            if serverResponse == "Le mot de passe est invalide. Veuillez réessayer.":
                print(serverResponse)

            elif serverResponse == "Password valid":
                validPassword = True

    #         password = util.inputpassword()
    #         sendMessageToServer(password)
    #
    #         serverResponse = receiveMessageFromServer()
    #         if serverResponse == "Le nom d'utilisateur est déjà utilisé. Veuillez réessayer.":
    #             print(serverResponse)
    #             continue
    #         elif serverResponse == "Le mot de passe est invalide. Veuillez réessayer.":
    #             print(serverResponse)
    #             continue
    #         else:
    #             createAccountSuccessful = True
    #
    # else:
    #     logIn()


# def main():
#
#     logInCommand = getLoginCommand()
#     if logInCommand == "1":
#         createAccount()
#     else:
#         logIn()
#
#     mainMenuCommand = getMainMenuCommand()
#     if mainMenuCommand == "1":
#         checkMails()
#     elif mainMenuCommand == "2":
#         sendMails()
#     elif mainMenuCommand == "3":
#         checkStats()
#     else:
#         quit()


if __name__ == "__main__":
    CLIENT_SOCKET = createSocket()
    main()
