import getpass
from hashlib import sha256
from os import path, mkdir
from re import search
import smtplib
from email.mime.text import MIMEText


def searchString(regex, string):
    return search(regex, string)


def hashPassword(password):
    return sha256(password.encode()).hexdigest()


def inputPassword():
    return getpass.getpass("Mot de passe: ")


def checkIfFileExists(filePath):
    return path.exists(filePath)


def createDirectory(name):
    mkdir(name)
    print("made dir")


def sendMail(sender, recipient, subject, message):
    msg = MIMEText(message)
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    smtpConnection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
    smtpConnection.sendmail(sender, recipient, msg.as_string())
    smtpConnection.quit()
