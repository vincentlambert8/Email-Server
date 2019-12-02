#!/usr/bin/python2.4
# -*- coding: utf-8 -*-

import socket
import util
import optparse
import sys


def getParserArgument():
    parser = optparse.OptionParser()
    parser.add_option("-p", "--port", dest="port", type=int, default=1400,
                        help="Port sur lequel envoyer et écouter les messages")
    return parser.parse_args(sys.argv[1:])[0]


def createUserConfigFile(username, password):
    createUserDirectory(username)

    filePath = f"{username}/config.txt"
    with open(filePath, "w") as file:
        hashedPassword = util.hashPassword(password)
        file.write(hashedPassword)


def createUserDirectory(username):
    util.createDirectory(username)


def passwordMatches(username, password):
    filePath = f"{username}/config.txt"
    with open(filePath, "r") as file:
        originalHash = file.readline()
        enteredHash = util.hashPassword(password)
        return originalHash == enteredHash


def logIn(serverSocket):
    validUsername = False
    while not validUsername:
        serverSocket.send("Nom d'utilisateur : ".encode())
        username = serverSocket.recv(1024).decode()
        if usernameIsValid(username):
            message = "Le nom d'utilisateur n'existe pas. Veuillez réessayer."
            serverSocket.send(message.encode())
        else:
            message = "Username valid"
            serverSocket.send(message.encode())
            validUsername = True

    validPassword = False
    while not validPassword:
        password = serverSocket.recv(1024).decode()
        if not passwordMatches(username, password):
            message = "Le mot de passe ne correspond pas au nom d'utilisateur. Veuillez réessayer."
            serverSocket.send(message.encode())
        else:
            message = "Password valid"
            serverSocket.send(message.encode())
            validPassword = True



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


# def startSocket(serverSocket):
#     serverSocket.listen(5)


# def createAccount(username, password):
#     createUserConfigFile(username, password)


def getLoginCommand(serverSocket):
    successfulCommand = False
    while not successfulCommand:
        message = ""
        showLogInMenu(serverSocket)
        logInCommand = serverSocket.recv(1024).decode()
        successfulCommand = checkLogInCommand(logInCommand)
        if not successfulCommand:
            #print("La commande entrée est invalide. Veuillez entrer un nombre de 1 à 2")
            message = "La commande entrée est invalide. Veuillez entrer un nombre de 1 à 2"
            serverSocket.send(message.encode())
        else:
            message = "Command successful"
            serverSocket.send(message.encode())

    return logInCommand


def showLogInMenu(serverSocket):
    # print("\nMenu de connexion")
    # print("1. Créer un compte")
    # print("2. Se connecter")
    connectionMenu = "\nMenu de connexion\n1. Créer un compte\n2. Se connecter"
    serverSocket.send(connectionMenu.encode())


def checkLogInCommand(logInCommand):
    return logInCommand == "1" or logInCommand == "2"


def createAccount(serverSocket):
    validUsername = False
    while not validUsername:
        serverSocket.send("Nom d'utilisateur : ".encode())
        username = serverSocket.recv(1024).decode()
        if not usernameIsValid(username):
            message = "Le nom d'utilisateur est déjà utilisé. Veuillez réessayer."
            serverSocket.send(message.encode())
        else:
            message = "Username valid"
            serverSocket.send(message.encode())
            validUsername = True

    validPassword = False
    while not validPassword:
        password = serverSocket.recv(1024).decode()
        if not passwordIsValid(password):
            message = "Le mot de passe est invalide. Veuillez réessayer."
            serverSocket.send(message.encode())
        else:
            message = "Password valid"
            serverSocket.send(message.encode())
            validPassword = True

    createUserConfigFile(username, password)
    #     username = serverSocket.recv(1024).decode()
    #     print("salut")
    #     serverSocket.send("Mot de passe : ".encode())
    #     password = serverSocket.recv(1024).decode()
    #     print("allo")
    #     if not usernameIsValid(username):
    #         message = "Le nom d'utilisateur est déjà utilisé. Veuillez réessayer."
    #         serverSocket.send(message.encode())
    #         continue
    #     elif not passwordIsValid(password):
    #         message = "Le mot de passe est invalide. Veuillez réessayer."
    #         serverSocket.send(message.encode())
    #         continue
    #     else:
    #         data = {"command": "signup", "username": username, "password": password}
    #         serverSocket.send(message.encode())
    #         createAccountSuccessful = True
    #
    # return data



def getAccountCredentials(serverSocket):
    username = getUsername(serverSocket)
    password = getpassword(serverSocket)

    return username, password


def getUsername(serverSocket):
    message = "Nom d'utilisateur : "
    serverSocket.send(message.encode())
    username = serverSocket.recv(1024).decode()
    return username


def getpassword(serverSocket):
    password = serverSocket.recv(1024).decode()
    return password


def main():
    serverSocket = createNewSocket()
    #startSocket(serverSocket)

    serverSocket.listen(5)

    while True:

        connection, address = serverSocket.accept()

        logInCommand = getLoginCommand(connection)
        if logInCommand == "1":
            createAccount(connection)

        else:
            logIn(connection)

        # accountData = eval(connection.recv(1024).decode())
        #
        # if accountData.get("command") == "login":
        #     if usernameIsValid(accountData.get("username")):
        #         message = "Le nom d'utilisateur n'existe pas. Veuillez réessayer."
        #         connection.send(message.encode())
        #     elif not passwordMatches(accountData.get("username"), accountData.get("password")):
        #         message = "Le mot de passe ne correspond pas au nom d'utilisateur. Veuillez réessayer."
        #         connection.send(message.encode())
        #     else:
        #         logIn(accountData.get("username"), accountData.get("password"))
        #
        # elif accountData.get("command") == "signup":
        #     if not usernameIsValid(accountData.get("username")):
        #         print("frette")
        #         message = "Le nom d'utilisateur est déjà utilisé. Veuillez réessayer."
        #         connection.send(message.encode())
        #     elif not passwordIsValid(accountData.get("password")):
        #         print("coton")
        #         message = "Le mot de passe est incorrect. Veuillez réessayer."
        #         connection.send(message.encode())
        #     else:
        #         print("ouatté")
        #         createAccount(accountData.get("username"), accountData.get("password"))


if __name__ == "__main__":
    PORT = getParserArgument().port
    main()
