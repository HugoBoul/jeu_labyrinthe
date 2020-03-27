# -*- coding: utf-8 -*
import socket
import select
from fonctions import *
from labyrinthe import *

hote = ''
port = 12800

print("python robot.py \n ")
print("Labyrinthes existants :")
print("1 - facile")
print("2 - prison \n")

numéro_labyrinthe = "0" #initialisation du labyrinthe avant choix joueur
#choix joueur entre facile ou prison
while (numéro_labyrinthe != "1" and numéro_labyrinthe != "2") == True:
    numéro_labyrinthe = input("Entrez un numéro de labyrinthe pour commencer à jouer : ")
    numéro_labyrinthe = numéro_labyrinthe.lower()
    if numéro_labyrinthe not in "12":
        print("Merci de saisir les numéros 1 ou 2 pour facile ou prison respectivement!")
    elif numéro_labyrinthe in "12":
        #chemin vers le répertoire cartes où se situent 2 répertoires facile & prison
        chemin_carte = os.getcwd() + "\\cartes"

        #toutes les cartes faciles sont dans le répertoire facile, les cartes prisons dans le répertoire prison
        #on enregistre dans la liste liste_carte_facile les fichiers de cartes faciles
        chemin_carte_facile = chemin_carte + "\\facile"
        
        liste_carte_facile = os.listdir(chemin_carte_facile)
        #on enregistre dans la liste liste_carte_prison les fichiers de cartes prisons
        chemin_carte_prison = chemin_carte + "\\prison" 
        liste_carte_prison = os.listdir(chemin_carte_prison)
        
        global ma_carte
        if numéro_labyrinthe == "1":
            ma_carte = choix_carte(liste_carte_facile, chemin_carte_facile)
        else:
            ma_carte = choix_carte(liste_carte_prison, chemin_carte_prison)

print("On attend les clients.")
                                
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

serveur_lance = True        
partie_terminée = False
partie_commencée = False

carte_clients = {}
robot_clients = {}
liste_clients = {}
mouvt_clients = {}
pcrea_clients = {}
mcrea_clients = {}

clients_connectes = []
numero_client = 0

# Initialisation du jeu avec le nombre maximum de joueur pour la carte sélectionnée
labyrinthe = Labyrinthe(numero_client)
nombre_joueur_max = labyrinthe.nombre_joueur_maximum(ma_carte)

while serveur_lance:
    # On va vérifier que de nouveaux clients ne demandent pas à se connecter
    # Pour cela, on écoute la connexion_principale en lecture
    # On attend maximum 50ms
    
    connexions_demandees, wlist, xlist = select.select([connexion_principale],
            [], [], 0.05)
    
    for connexion in connexions_demandees:
        connexion_avec_client, infos_connexion = connexion.accept()
        
        if partie_commencée == False:
            
            if len(clients_connectes) < nombre_joueur_max:
           
                # On ajoute le socket connecté à la liste des clients
                clients_connectes.append(connexion_avec_client)
                numero_client += 1
                
                # On initie la création de la carte des nouveaux joueurs à partir de la carte du dernier joueur connecté!
                labyrinthe = Labyrinthe(numero_client)
                # On crée le nouveau robot en X (en indice_X)
                # On met les autres robots en x
                # On indexe la carte dans liste et on récupère sa taille et l'indice du X
                liste, indice_X = labyrinthe.creation_derniere_carte(ma_carte)
                # On reconstruit la partie à partir de liste
                partie = labyrinthe.formatage_derniere_carte(liste)
                
                # On stocke les attributs de la partie créée
                carte_clients[numero_client] = partie # Partie des nouveaux clients
                liste_clients[numero_client] = liste # Liste du jeu des nouveaux clients
                robot_clients[numero_client] = indice_X # Indice du Robot des nouveaux clients
                mouvt_clients[numero_client] = " " # Symbole où se trouve le robot (une porte ou un vide)
                pcrea_clients[numero_client] = -1 # Indice d'une porte créée
                mcrea_clients[numero_client] = -1 # Indice d'un mur créé
                
                # On redéfinit cette partie comme étant la dernière créée
                ma_carte = partie 
                
                # On ajoute le nouveau robot dans les cartes précédentes
                # (on met x à la place du X du dernier joueur)
                if numero_client >=2:
                    elt = 1
                    while elt < numero_client:
                        liste_clients[elt][indice_X] = labyrinthe.ajout_robot_adverse(liste_clients[elt][indice_X])
                        carte_clients[elt] = labyrinthe.formatage_derniere_carte(liste_clients[elt])
                        elt +=1
                    
                # On communique aux clients
                compteur = 0
                for client in clients_connectes:
                
                    compteur +=1
                    # On dit bonjour au client qui se connecte
                    msg_emis = "\nBienvenue, joueur " + repr(numero_client) + "\n"
                    
                    # On envoie la carte
                    msg_emis = msg_emis + "\n" + carte_clients[compteur]
                    
                    # On l'invite à commencer à jouer si plus de 2 clients sont connectés
                    if numero_client >= 2:
                        msg_emis = msg_emis + "\nEntrez C pour commencer à jouer :"
                        print("plus d'un joueur, invitation à commencer la partie envoyée")
                    client.send(msg_emis.encode())
                    print("carte envoyée")
            else:
                # Gestion des cas où un client se connecte mais la carte n'a plus d'espaces vides pour 1 robot!
                msg_emis = "La partie a atteint le nombre maximum de joueur!"
                connexion_avec_client.send(msg_emis.encode())
    
        # Gestion des cas où un client se connecte et la partie a déjà commencé  
        else:
            # On ajoute le socket connecté à la liste des clients tardifs
            clients_tardifs = []
            clients_tardifs.append(connexion_avec_client)
            
            for client in clients_tardifs:
                msg_emis = "La partie a déjà commencé!"
                client.send(msg_emis.encode())
    
    # Maintenant, on écoute la liste des clients connectés
    # Les clients renvoyés par select sont ceux devant être lus (recv)
    # On attend là encore 50ms maximum
    # On enferme l'appel à select.select dans un bloc try
    # En effet, si la liste de clients connectés est vide, une exception
    # Peut être levée
    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes,
                [], [], 0.05)
    except select.error:
        if partie_commencée == True:
            print("Erreur dans la réception des commandes des clients!")
        pass
    else:
        if partie_commencée == False:
            # On parcourt la liste des clients à lire
            compteur = 0
            
            # On récupère c ou C normalement
            for client in clients_a_lire:
                msg_reçu = client.recv(1024)
                msg_reçu = msg_reçu.decode()
                
                # On envoie le msg que la partie commence
                if msg_reçu.lower() == "c":
                    print("Message reçu <{}>".format(msg_reçu))
                    for client in clients_connectes:
                        msg_emis = "Partie commencée! Merci d'attendre votre tour..."
                        client.send(msg_emis.encode())
                    print("Partie commencée envoyé à tous!") 
                    partie_commencée = True
                    
                    # On invite le premier joueur à jouer (le 1er connecté)
                    msg_emis = "A vous de jouer!"
                    clients_connectes[compteur].send(msg_emis.encode())
                    compteur +=1
                    print("Tour de joueur envoyé à client {}".format(compteur))
        
        # On récupère les commandes de jeu normalement
        
        elif partie_commencée == True:
        # On envoie la carte à tout le monde suite au coup du joueur 1
        # On envoie le message du tour au joueur 2, une fois que le joueur 1 joue etc.
        
            for client in clients_a_lire:
                msg_reçu = client.recv(1024)
                msg_reçu = msg_reçu.decode()
                print("Message reçu <{}>".format(msg_reçu))
                
                if client == clients_connectes[compteur-1]: # le joueur 1 a joué
                    
                    # On réinitialise la position initiale du robot du joueur dans les autres cartes
                    elt = 1
                    while elt <= numero_client:
                        if elt != compteur:
                            liste_clients[elt][robot_clients[compteur]] = mouvt_clients[compteur]
                        elt +=1
                    
                    # On récupère la nouvelle liste (#proxy_deplacement est introduit pour aider aux tests unitaires seulement)
                    liste_clients[compteur], robot_clients[compteur], mouvt_clients[compteur], pcrea_clients[compteur], mcrea_clients[compteur], msg, proxy_deplacement = \
						labyrinthe.modifier_carte(msg_reçu, liste_clients[compteur], robot_clients[compteur], mouvt_clients[compteur])
                    print(msg)
                    # On la formate en nouvelle carte
                    carte_clients[compteur] = labyrinthe.formatage_derniere_carte(liste_clients[compteur])
                    
                    # On ajoute le robot dans les cartes des autres joueurs ainsi que les nouvelles portes ou nouveaux murs
                    elt = 1
                    while elt <= numero_client:
                        if elt != compteur:
                            liste_clients[elt][robot_clients[compteur]] = labyrinthe.ajout_robot_adverse(liste_clients[elt][robot_clients[compteur]])
                            if pcrea_clients[compteur] != -1:
                                liste_clients[elt][pcrea_clients[compteur]] = labyrinthe.ajout_porte(liste_clients[elt][pcrea_clients[compteur]])
                            if mcrea_clients[compteur] != -1:
                                liste_clients[elt][mcrea_clients[compteur]] = labyrinthe.ajout_mur(liste_clients[elt][mcrea_clients[compteur]])
                            carte_clients[elt] = labyrinthe.formatage_derniere_carte(liste_clients[elt])
                        elt +=1
                    
                    # Réinitialisation de prcrea et mcrea
                    pcrea_clients[compteur] = -1
                    mcrea_clients[compteur] = -1
                    
                    # Vérification de la victoire
                    victoire = labyrinthe.victoire(mouvt_clients[compteur])
                    if victoire:
                        msg = "Bravo joueur " + repr(compteur) + "! Vous avez gagné!"
                        
                    # On envoie la carte de tous les joueurs
                    elt = 1
                    for client in clients_connectes:
                        if elt == compteur:
                            msg_emis = "\n" + msg + "\n" + carte_clients[elt]
                        else:
                            msg_emis = "\nCarte du joueur " + repr(compteur) + "\n" + msg + "\n" + carte_clients[elt]
                        client.send(msg_emis.encode())
                        elt +=1
                    print("Coup du joueur {} envoyé à tout le monde!".format(compteur))
                    
                    if not victoire:
                        # cela permet de boucler sur tous les joueurs après chaque tour
                        if compteur == numero_client:
                            compteur = 1
                            msg_emis = "A vous de jouer!"
                            clients_connectes[compteur-1].send(msg_emis.encode())
                            print("Tour de joueur envoyé à client {}".format(compteur))
                            break
                        
                        # On envoie le tour 
                        if compteur < numero_client:
                            msg_emis = "A vous de jouer!"
                            clients_connectes[compteur].send(msg_emis.encode())
                            print("Tour de joueur envoyé à client {}".format(compteur+1))
                            compteur +=1 # pour passer au joueur suivant
