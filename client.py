
# -*- coding: utf-8 -*
import socket, threading, sys

""" 2 thread fonctionnent en parallèle :
- la réception des messages du serveur : thread_reception
- l'envoi de messages (commandes de jeu) du client au serveur : thread_emission_début_partie
NB : thread_emission_début_partie est lancée par thread_reception quand 2 joueurs sont connectés """

hote = "localhost"
port = 12800

class reception_msg(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
        self.partie_commencée = False
        self.tour_joueur = False
        self.partie_terminée = False
        
    def run(self):
        while 1:
            msg_reçu = self.connexion.recv(1024)
            print("{0}".format(msg_reçu.decode()))
            if "Entrez C" in msg_reçu.decode():
                # Ce thread va tourner
                # Il permet aux joueurs de saisir "C" et les commandes de jeu
                thread_emission_début_partie = emission_msg(self.connexion)
                thread_emission_début_partie.start()
            if "commencée" in msg_reçu.decode():
                self.partie_commencée = True
            if "A vous de jouer" in msg_reçu.decode():
                self.tour_joueur = True
            if "Bravo" in msg_reçu.decode():
                self.partie_terminée = True
        
    def bloquer_tour(self):
        self.tour_joueur = False
        
class emission_msg(reception_msg):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
        self.TR = thread_reception
        
    def run(self):
        
        while 1:
            msg = input()
            if msg.lower() == "c" and self.TR.partie_commencée == False:
                self.connexion.send(msg.encode())
                print("Commande envoyée au serveur!")
            elif msg.lower() != "c" and self.TR.partie_commencée == False:
                print("Commande non autorisée : merci d'entrer C pour commencer la partie!")
            elif msg.lower() == "c" and self.TR.partie_commencée == True:
                print("Partie déjà commencée!")
            elif self.TR.tour_joueur == False and self.TR.partie_terminée == False:
                print("Ce n'est pas votre tour!")
            elif self.TR.partie_terminée == True:
                print("Partie terminée!")
            elif msg.lower()[0] in "nseo" and len(msg) == 1:
                self.connexion.send(msg.encode())
                print("Commande envoyée au serveur!")
                self.TR.bloquer_tour()
            elif msg.lower()[0] in "nseo" and msg[1:].isnumeric() == True:
                self.connexion.send(msg.encode())
                print("Commande envoyée au serveur!")
                self.TR.bloquer_tour()
            elif len(msg) == 2 and msg.lower()[0] in "mp" and msg.lower()[1] in "nseo":
                self.connexion.send(msg.encode())
                print("Commande envoyée au serveur!")
                self.TR.bloquer_tour()
            else:
                print("Commande non autorisée")
                 
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("En attente de connexion avec le serveur...")
try:
    connexion_avec_serveur.connect((hote, port))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()    
print("Connexion établie avec le serveur.")

thread_reception = reception_msg(connexion_avec_serveur) 
thread_reception.start()








