import getpass
from hashlib import sha256
from os import path, mkdir, listdir
from re import search
import smtplib
from email.mime.text import MIMEText


def searchString(regex, string):
    return search(regex, string)


def hashPassword(password):
    return sha256(password.encode()).hexdigest()


def inputpassword():
    return getpass.getpass("Mot de passe: ")


def checkIfFileExists(filePath):
    return path.exists(filePath)


def createDirectory(name):
    mkdir(name)


def sendMail(sender, recipient, msg):

    smtpConnection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
    smtpConnection.sendmail(sender, recipient, msg.as_string())
    smtpConnection.quit()


def getMessageAsMIME(sender, recipient, subject, message):
    msg = MIMEText(message)
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    return msg


def getNumberOfFilesInDirectory(directoryPath):
    return len([name for name in listdir(directoryPath)])


def getDirectorySize(directoryPath):
    return path.getsize(directoryPath)
