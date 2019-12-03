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


def passwordMatches(password, filePath):
    with open(filePath, "r") as file:
        originalHash = file.readline()
        enteredHash = util.hashPassword(password)
        return originalHash == enteredHash
    

def sendMessageToClient(message):
    CONNECTION.send(message.encode())


def logIn(username, password):
    successfulLogIn = False
    successfulLogIn, message = tryToLogIn(username, password)
    data = {"status": successfulLogIn, "message": message}
    sendMessageToClient(str(data))

    return successfulLogIn


def tryToLogIn(username, password):
    filePath = f"{username}/config.txt"

    if not util.checkIfFileExists(filePath):
        message = "Le nom d'utilisateur entré n'existe pas. Veuillez recommencer"
        return False, message

    if not passwordMatches(password, filePath):
        message = "Le mot de passe entré est invalide. Veuillez recommencer"
        return False, message

    message = f"Bienvenue {username}"
    return True, message


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


def createAccount(username, password):
    accountCreated = False
    if username == "":
        data = {"status": False, "message": "Le nom d'utilisateur est vide. Veuillez recommencer"}
        sendMessageToClient(str(data))

    elif accountExists(username):
        data = {"status": False, "message": "Le nom d'utilisateur entré est déjà utilisé. Veuillez recommencer"}
        sendMessageToClient(str(data))

    else:
        createUserConfigFile(username, password)
        data = {"status": True, "message": "Compte créé avec succès"}
        sendMessageToClient(str(data))
        accountCreated = True

    return accountCreated


def accountExists(username):
    return util.checkIfFileExists(f"{username}/config.txt")


def checkLogInCommand(logInCommand):
    return logInCommand == "1" or logInCommand == "2"


def getNumberOfMails(recipient):
    directoryPath = f"{recipient}/"
    return util.getNumberOfFilesInDirectory(directoryPath) - 1


def createMailFile(filePath, msg):

    with open(filePath, "w") as file:
        file.write(msg.as_string())


def sendLocalMail(recipient, msg):
    directoryPath = ""

    if not util.checkIfFileExists(f"{recipient}/config.txt"):
        directoryPath = "ERREUR/"
        data = {"status": False, "message": "Le destinataire n'existe pas. Le message a été déposé dans le dossier "
                                            "'ERREUR'."}
        sendMessageToClient(str(data))

    else:
        directoryPath = f"{recipient}/"
        data = {"status": True, "message": "Le courriel a bien été envoyé."}
        sendMessageToClient(str(data))

    numberOfMails = getNumberOfMails(recipient)
    print(f"number of mail: {numberOfMails}")
    filePath = f"{directoryPath}/{numberOfMails + 1}"
    createMailFile(filePath, msg)


def sendOutsideMail(sender, recipient, msg):
    try:
        util.sendMail(sender, recipient, msg)
    except:
        data = {"status": False, "message": "Le courriel n'a pas pu être envoyé. Veuillez recommencer"}
    else:
        data = {"status": True, "message": f"Le courriel a été envoyé avec succès à {recipient}."}
    finally:
        sendMessageToClient(str(data))


def sendMail(sender, recipient, subject, body):
    recipientHost = recipient.split('@')[1]
    print(recipient)
    print(recipientHost)
    msg = util.getMessageAsMIME(sender, recipient, subject, body)

    if recipientHost == "glo2000.ca":
        sendLocalMail(recipient, msg)
    else:
        sendOutsideMail(sender, recipient, msg)


def main():
    # Login/Signup loop
    while True:
        accountData = eval(CONNECTION.recv(1024).decode())

        if accountData.get("command") == "login":
            if logIn(accountData.get("username"), accountData.get("password")):
                break

        elif accountData.get("command") == "signup":
            if createAccount(accountData.get("username"), accountData.get("password")):
                break

    # Main menu loop
    while True:
        commandData = eval(CONNECTION.recv(1024).decode())

        if commandData.get("command") == "sendMail":
            sender = commandData.get("sender")
            recipient = commandData.get("recipient")
            subject = commandData.get("subject")
            body = commandData.get("body")

            sendMail(sender, recipient, subject, body)

        elif commandData.get("command") == "checkMails":
            checkMails()

        elif commandData.get("command") == "stats":
            showStats()

        elif commandData.get("command") == "quit":
            break


def startSocket(serverSocket):
    print("Starting server...")
    serverSocket.listen(5)
    print(f"Listening on port {PORT}")


if __name__ == "__main__":
    PORT = getParserArgument().port
    SERVER_SOCKET = createNewSocket()
    startSocket(SERVER_SOCKET)
    while True:
        CONNECTION, ADDRESS = SERVER_SOCKET.accept()
        main()
