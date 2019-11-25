#!/usr/bin/python2.4
# -*- coding: utf-8 -*-

class Client:
    def __init__(self, username):
        pass









def showLogInMenu():
    print("Menu de connexion")
    print("1. Créer un compte")
    print("2. Se connecter")

def showMainMenu():
    print("Menu principal")
    print("1. Consultation de courriels")
    print("2. Envoi de courriels")
    print("3. Statistiques")
    print("4. Quitter")

def checkLogIn(logInCommand):
    if logInCommand == 1:
        createAccount()
    elif logInCommand == 2:
        logIn()
    else:
        raise ValueError("Something other than 1 or 2 was entered")

def createAccount():
    showCreateAccounteMenu()
    


def main():

    while (True):
        showLogInMenu()
        try:
            checkLogIn(input())
        except ValueError:
            print("\nErreur: Veuillez entrer 1 ou 2\n")
        else:
            break

if __name__ == "__main__":
    main()
