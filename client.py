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
    username, password = getAccountCredentials()
    data = {"command": "signup", "username": username, "password": password}
    message = str(data)

    sendMessageToServer(message)
    return username


def logIn():
    username, password = getAccountCredentials()
    data = {"command": "login", "username": username, "password": password}
    message = str(data)

    sendMessageToServer(message)
    return username


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
            print("La commande entrée est invalide. Veuillez entrer un nombre de 1 à 2.")

    return logInCommand


def getMainMenuCommand():
    successfulCommand = False
    while not successfulCommand:
        showMainMenu()
        mainMenuCommand = input()
        successfulCommand = checkMainMenuCommand(mainMenuCommand)
        if not successfulCommand:
            print("La commande entrée est invalide. Veuillez entrer un nombre de 1 à 4.")

    return mainMenuCommand


def createSocket():
    port = getparserArgument().port
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(("localhost", port))
    return clientSocket


def sendMessageToServer(message):
    CLIENT_SOCKET.send(message.encode())


def receiveMessageFromServer():
    data = CLIENT_SOCKET.recv(2048).decode()
    return data


def getMails(username):
    data = {"command": "checkMails", "username": username}
    sendMessageToServer(str(data))

    serverResponse = eval(receiveMessageFromServer())
    if not serverResponse.get("status"):
        print('\n' + serverResponse.get("message"))
        return False

    return serverResponse.get("mailList")


def showMail(mailContent):
    for key in mailContent:
        print(mailContent.get(key))


def showInbox(mails, numberOfMails):
    print(f"\nVotre boite de réception contient {numberOfMails} messages: ")
    for i in range(1, len(mails) + 1):
        subject = mails.get(i).get("subject")
        print(f"{i} - {subject[8:]}")


def showMails(mails):
    numberOfMails = len(mails)
    while True:
        showInbox(mails, numberOfMails)
        mailNumber = input("\nEntrer le numéro du courriel pour le consulter: ")
        try:
            mailNumber = int(mailNumber)
        except:
            print("\nLa commande entrée n'est pas un nombre. Veuillez recommencer.")
            continue
        else:
            if mailNumber < 0 or mailNumber > numberOfMails:
                print(f"Le numéro entré n'est pas compris entre 1 et {numberOfMails}. Veuillez recommencer.")
                continue

            print()
            showMail(mails.get(mailNumber))

            print("\nVoulez-vous consulter un autre courriel ? (Oui ou Non)")
            command = input()

            if command.lower() == "non":
                break


def checkMails(username):
    mails = getMails(username)
    if not mails:
        return

    showMails(mails)


def endConnection():
    data = {"command": "quit"}
    sendMessageToServer(str(data))
    quit()


def sendMail(username):
    recipient = input("Adresse de destination: ")
    subject = input("Objet du message: ")
    print("Corps du message:")
    body = input("")
    data = {"command": "sendMail", "sender": username, "recipient": recipient, "subject": subject, "body": body}

    print("\nLe message est en cours d'envoi. Cela peut prendre quelques secondes.")
    sendMessageToServer(str(data))


def getStats(username):
    data = {"command": "checkStats", "username": username}
    sendMessageToServer(str(data))
    serverResponse = eval(receiveMessageFromServer())
    return serverResponse


def checkStats(username):
    stats = getStats(username)
    showStats(stats)


def showStats(stats):
    username = stats.get("username")
    numberOfMails = stats.get("numberOfMails")
    directorySize = stats.get("directorySize")
    mailList = stats.get("mailList")

    print('\n' + f"------- Information sur l'utilisateur {username} -------\n")
    print(f"Votre boite contient {numberOfMails} courriel(s).")
    print(f"La taille totale de la boite de courriels est de {directorySize} octets.")
    print("Voici une liste des courriels dans la boite:")
    for i in range(1, len(mailList) + 1):
        subject = mailList.get(i)
        print(f"{i} - {subject}")

    input("\nAppuyer sur Entrée pour revenir au menu...")


def main():
    username = ""

    logInLoop = True
    while logInLoop:
        logInCommand = getLoginCommand()
        if logInCommand == "1":
            username = createAccount()

        elif logInCommand == "2":
            username = logIn()

        serverResponse = eval(receiveMessageFromServer())
        print('\n' + serverResponse.get("message"))
        logInLoop = not serverResponse.get("status")

    while True:
        mainMenuCommand = getMainMenuCommand()
        if mainMenuCommand == "1":
            checkMails(username)
            continue

        elif mainMenuCommand == "2":
            sendMail(username)

        elif mainMenuCommand == "3":
            checkStats(username)
            continue

        elif mainMenuCommand == "4":
            endConnection()

        serverResponse = eval(receiveMessageFromServer())
        print('\n' + serverResponse.get("message"))


if __name__ == "__main__":
    CLIENT_SOCKET = createSocket()
    main()
