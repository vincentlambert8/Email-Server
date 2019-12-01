#!/usr/bin/python2.4
# -*- coding: utf-8 -*-

import socket
import util
import argparse


def getParserArgument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", dest="port", type=int, default=1400,
                        help="Port sur lequel envoyer et écouter les messages")
    return parser.parse_args()


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
    message = ""

    filePath = f"{username}/config.txt"
    if not util.checkIfFileExists(filePath):
        message = "Le nom d'utilisateur entré n'existe pas. Veuillez recommencer"
        return False
    if not passwordMatches(password, filePath):
        message = "Le mot de passe entré est invalide. Veuillez recommencer"
        return False
    return True


def usernameIsValid(username):
    path = f"{username}/config.txt"
    return not util.checkIfFileExists(path)


def passwordIsValid(password):
    regex = "^(?=.*[a-z])(?=.*[A-Z])(?=(.*?\d){2})[a-zA-Z\d]{6,12}$"
    return util.searchString(regex, password)


def emailAddressIsValid(address):
    regex = r"^[^@]+@[^@]+\.[^@]+$"
    return util.searchString(regex, address)


def createNewSocket():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(("localhost", PORT))
    return serverSocket


def startSocket(serverSocket):
    serverSocket.listen(5)


def createAccount(username, password):
    createUserDirectory(username, pasword)


def main():
    serverSocket = createNewSocket()
    startSocket(serverSocket)

    connection, address = serverSocket.accept()

    accountData = dict(connection.recv(1024))

    if accountData.get("command") == "login":
        logIn(accountData.get("username"), accountData.get("password"))

    elif accountData.get("command" == "signup"):
        createAccount(accountData.get("username"), accountData.get("password"))


if __name__ == "__main__":
    PORT = getParserArgument().port
    main()


def launchServerSocket(serverSocket):
    serverSocket.listen(5)
    print("Démarrage du serveur...")
    print("Listening on port " + str(serverSocket.getsockname()[1]))

    while True:  # Boucle connexion
        # Le client se connecte au serveur
        # s est un socket pour interagir avec le client
        (s, address) = serverSocket.accept()

        clientIdentified = False

        while not clientIdentified:  # Boucle identification
            loginChoice = s.recv(1024).decode()
            if loginChoice == "1":
                username = s.recv(1024).decode()
                if not usernameIsValid(username):
                    errorMessage = "Ce nom d'utilisateur existe déjà. Veuillez rééssayer."
                    s.send(errorMessage.encode())
                    continue

                password = s.recv(1024).decode()
                if not passwordIsValid(password):
                    errorMessage = "Le mot de passe est invalide. Veuillez rééssayer."
                    s.send(errorMessage.encode())
                    continue
                    # TODO Faire en sorte que le serveur se souvient du username si le mot de passe est invalide

                clientIdentified = True

            elif loginChoice == "2":
                username = s.recv(1024).decode()
