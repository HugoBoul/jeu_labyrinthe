# -*- coding: utf-8 -*
import unittest, os, socket, random
from fonctions import *
from labyrinthe import Labyrinthe

""" A lancer depuis la console Windows avec : 'py -m unittest' """

class test_td(unittest.TestCase):
    """ Vérification de la constitution d'un labyrinthe standard

    Vérification de la création d'un labyrinthe depuis une chaîne

    Vérification des fonctionnalités du jeu multi-joueurs """
    test_path = os.getcwd()
    hote = ''
    port = 12800
    
    @classmethod
    def setUpClass(cls):
        cls.connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.connexion_principale.bind((cls.hote, cls.port))
        cls.connexion_principale.listen(5)
        print("Le serveur écoute à présent sur le port {}".format(cls.port))
    
    @classmethod
    def tearDownClass(cls):
        cls.connexion_principale.close()
        print("Le serveur s'est fermé!")
    
    def setUp(self):
        
        self.chemin_carte = self.test_path + "\\cartes"
        self.chemin_carte_facile = self.chemin_carte + "\\facile"
        self.liste_carte_facile = os.listdir(self.chemin_carte_facile)
        self.chemin_carte_prison = self.chemin_carte + "\\prison"
        self.liste_carte_prison = os.listdir(self.chemin_carte_prison)
        self.mur = "O"
        self.porte = "."
        self.sortie = "U"
        self.robot = "X"
        self.robot_adverse = "x"
        self.vide = " "
    
    def test_choix_carte(self):
        """ Vérification de la constitution d'un labyrinthe standard
        => vérification de la fonction choix_carte dans le module fonctions """
        
        # récupération des cartes
        liste_carte_facile = []
        liste_carte_prison = []
        
        # pour prendre en compte toutes les cartes
        for i, elt_facile in enumerate(self.liste_carte_facile):
            # Présence des symboles dans la carte facile
            carte_facile = choix_carte([self.liste_carte_facile[i]], self.chemin_carte_facile)
            liste_carte_facile.append(carte_facile)
            
            print("Carte facile " + str(i+1) + " :\n" + carte_facile + "\n")
            
            self.assertIn(self.mur, carte_facile)
            self.assertIn(self.porte, carte_facile)
            self.assertIn(self.sortie, carte_facile)
            self.assertNotIn(self.robot, carte_facile)
            self.assertIn(self.vide, carte_facile)
            self.assertNotIn(self.robot_adverse, carte_facile)
            
            # Vérification qu'il n'y a que les symboles attendus dans la carte facile
            symboles = self.mur + self.porte + self.sortie + self.robot + self.vide + "\n"
            for elt in carte_facile:
                self.assertIn(elt, symboles)
        
        # pour prendre en compte toutes les cartes
        for j, elt_prison in enumerate(self.liste_carte_prison):
        
            # Présence des symboles dans la carte prison
            carte_prison = choix_carte([self.liste_carte_prison[j]], self.chemin_carte_prison)
            liste_carte_prison.append(carte_prison)
            
            print("Carte prison " + str(j+1) + " :\n" + carte_prison + "\n")
            
            self.assertIn(self.mur, carte_prison)
            self.assertIn(self.porte, carte_prison)
            self.assertIn(self.sortie, carte_prison)
            self.assertNotIn(self.robot, carte_prison)
            self.assertIn(self.vide, carte_prison)
            self.assertNotIn(self.robot_adverse, carte_prison)
   
            # Vérification qu'il n'y a que les symboles attendus dans la carte prison
            for elt in carte_prison:
                self.assertIn(elt, symboles)

        # Vérification que les cartes facile et prison sont différentes
        for i, elt_facile in enumerate(liste_carte_facile):
            for j, elt_prison in enumerate(liste_carte_prison):
                self.assertNotEqual(elt_facile, elt_prison)
        
    def test_creation_labyrinthe_depuis_chaine(self):
        """ Vérification de la création d'un labyrinthe depuis une chaîne
        => vérification des méthodes de classe suivantes :
            - creation_derniere_carte 
            - formatage_derniere_carte """  
        # Vérification de creation_derniere_carte

        # Plus besoin de vérifier facile & prison
        
        i = 1 # On prend la deuxième carte facile (nombre maximum de joueur = 2)
        
        carte = choix_carte([self.liste_carte_facile[i]], self.chemin_carte_facile)
        
        print("La chaîne testée est :\n" + carte + "\n")
        
        numero_client = 1 # Initialisation du numero_client
        
        labyrinthe = Labyrinthe(numero_client)
        
        # Traitement du cas où l'on n'a plus de vide pour créer le robot!
        if numero_client <= labyrinthe.nombre_joueur_maximum(carte): 
            liste_1, indice_X_1 = labyrinthe.creation_derniere_carte(carte)
            carte_1 = labyrinthe.formatage_derniere_carte(liste_1)
            
            print("Le labyrinthe du client " + str(numero_client) + " est :\n" + carte_1 + "\n")
            
            self.assertNotEqual(carte, carte_1)
            self.assertEqual(numero_client, labyrinthe.nb_robot)
            self.assertEqual(liste_1[indice_X_1], self.robot)
            self.assertNotIn(self.robot_adverse, carte_1)

            # Vérification que la différence entre carte et carte_1 est le robot ajouté
            carte_1_transforme = carte_1.replace(self.robot, self.vide)
            self.assertEqual(carte, carte_1_transforme)
        else:
            with self.assertRaises(IndexError):
                labyrinthe.creation_derniere_carte(carte)
        
        numero_client = 2
        carte_2 = carte_1
        
        labyrinthe = Labyrinthe(numero_client)
        
        # Traitement du cas où l'on n'a plus de vide pour créer le robot!
        if numero_client <= labyrinthe.nombre_joueur_maximum(carte):
            liste_2, indice_X_2 = labyrinthe.creation_derniere_carte(carte_2)
            carte_2 = labyrinthe.formatage_derniere_carte(liste_2)
            
            print("Le labyrinthe du client " + str(numero_client) + " est :\n" + carte_2 + "\n")
            
            self.assertNotEqual(carte_1, carte_2)
            self.assertEqual(numero_client, labyrinthe.nb_robot)
            self.assertEqual(liste_2[indice_X_2], self.robot)
            self.assertIn(self.robot_adverse, carte_2)
            
            # Vérification que la différence entre carte_1 et carte_2 est le robot ajouté
            carte_2_transforme = carte_2.replace(self.robot, self.vide)
            carte_2_transforme = carte_2_transforme.replace(self.robot_adverse, self.robot)
            self.assertEqual(carte_1, carte_2_transforme)
        else:
            with self.assertRaises(IndexError):
                labyrinthe.creation_derniere_carte(carte_2)
                
        numero_client = 3
        carte_3 = carte_2

        labyrinthe = Labyrinthe(numero_client)
        
        # Traitement du cas où l'on n'a plus de vide pour créer le robot!
        if numero_client <= labyrinthe.nombre_joueur_maximum(carte):
            liste_3, indice_X_3 = labyrinthe.creation_derniere_carte(carte_3)
            carte_3 = labyrinthe.formatage_derniere_carte(liste_3)
            
            print("Le labyrinthe du client " + str(numero_client) + " est :\n" + carte_3 + "\n")
            
            self.assertNotEqual(carte_2, carte_3)
            self.assertEqual(numero_client, labyrinthe.nb_robot)
            self.assertEqual(liste_3[indice_X_3], self.robot)
            self.assertIn(self.robot_adverse, carte_3)
            
            # Vérification que la différence entre carte_2 et carte_3 est le robot ajouté
            carte_3_transforme = carte_3.replace(self.robot, self.vide)
            carte_2_transforme = carte_2.replace(self.robot, self.robot_adverse)
            self.assertEqual(carte_2_transforme, carte_3_transforme)
        else:
            with self.assertRaises(IndexError):
                labyrinthe.creation_derniere_carte(carte_3)
        # Par récurrence on valide à numéro_client > 3
        
        
    def test_fonctionnalites_jeu_multi_joueurs(self):
        """ Vérification des fonctionnalités du jeu multi-joueurs """
        # Plus besoin de vérifier la création du labyrinthe à partir d'une chaîne
        # Création de 3 labyrinthes avec 3 joueurs connectés
        
        # Initialisation des éléments des labyrinthe pour le jeu multi-joueurs :
        carte_clients = {}
        robot_clients = {}
        liste_clients = {}
        mouvt_clients = {}
        pcrea_clients = {}
        mcrea_clients = {}
        
        i = -1 # On prend la première carte prison (nombre maximum de joueur important!)
        
        carte = choix_carte([self.liste_carte_prison[i]], self.chemin_carte_prison)
        
        print("La carte (prison) de ce test est :\n" + carte + "\n")

        # Connexion du client 1
        connexion_avec_serveur_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.assertIsNotNone(connexion_avec_serveur_1)

        connexion_avec_serveur_1.connect(("localhost", self.port))
        
        numero_client = 1 # Initialisation du numero_client
        
        labyrinthe = Labyrinthe(numero_client)
        
        liste_1, indice_X_1 = labyrinthe.creation_derniere_carte(carte)
        carte_1 = labyrinthe.formatage_derniere_carte(liste_1)
        
        carte_clients[1] = carte_1 # Partie des nouveaux clients
        liste_clients[1] = liste_1 # Liste du jeu des nouveaux clients
        robot_clients[1] = indice_X_1 # Indice du Robot des nouveaux clients
        mouvt_clients[1] = " " # Symbole où se trouve le robot (une porte ou un vide)
        pcrea_clients[1] = -1 # Indice d'une porte créée
        mcrea_clients[1] = -1 # Indice d'un mur créé
        
        # Connexion du client 2
        connexion_avec_serveur_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.assertIsNotNone(connexion_avec_serveur_2)

        connexion_avec_serveur_2.connect(("localhost", self.port))
        
        numero_client = 2
        carte_2 = carte_1
        
        labyrinthe = Labyrinthe(numero_client)

        liste_2, indice_X_2 = labyrinthe.creation_derniere_carte(carte_2)
        carte_2 = labyrinthe.formatage_derniere_carte(liste_2)
        
        # Ajout du robot du client 2 dans carte_1
        liste_clients[1][indice_X_2] = labyrinthe.ajout_robot_adverse(liste_clients[1][indice_X_2])
        carte_clients[1] = labyrinthe.formatage_derniere_carte(liste_clients[1])
        carte_1 = carte_clients[1]
        
        carte_clients[2] = carte_2 # Partie des nouveaux clients
        liste_clients[2] = liste_2 # Liste du jeu des nouveaux clients
        robot_clients[2] = indice_X_2 # Indice du Robot des nouveaux clients
        mouvt_clients[2] = " " # Symbole où se trouve le robot (une porte ou un vide)
        pcrea_clients[2] = -1 # Indice d'une porte créée
        mcrea_clients[2] = -1 # Indice d'un mur créé

        # Connexion du client 3
        connexion_avec_serveur_3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.assertIsNotNone(connexion_avec_serveur_3)

        connexion_avec_serveur_3.connect(("localhost", self.port))
                
        numero_client = 3
        carte_3 = carte_2

        labyrinthe = Labyrinthe(numero_client)
       
        liste_3, indice_X_3 = labyrinthe.creation_derniere_carte(carte_3)
        carte_3 = labyrinthe.formatage_derniere_carte(liste_3)
        
        # Ajout du robot du client 3 dans carte_1 et carte_2
        liste_clients[1][indice_X_3] = labyrinthe.ajout_robot_adverse(liste_clients[1][indice_X_3])
        carte_clients[1] = labyrinthe.formatage_derniere_carte(liste_clients[1])
        liste_clients[2][indice_X_3] = labyrinthe.ajout_robot_adverse(liste_clients[2][indice_X_3])
        carte_clients[2] = labyrinthe.formatage_derniere_carte(liste_clients[2])
        
        # Réinitialisation de carte 1 & 2
        carte_1 = carte_clients[1]
        carte_2 = carte_clients[2]
        
        print("Carte 1 (du client 1) :\n" + carte_1 + "\n")
        print("Carte 2 (du client 2) :\n" + carte_2 + "\n")
        print("Carte 3 (du client 3) :\n" + carte_3 + "\n")
        
        carte_clients[3] = carte_3 # Partie des nouveaux clients
        liste_clients[3] = liste_3 # Liste du jeu des nouveaux clients
        robot_clients[3] = indice_X_3 # Indice du Robot des nouveaux clients
        mouvt_clients[3] = " " # Symbole où se trouve le robot (une porte ou un vide)
        pcrea_clients[3] = -1 # Indice d'une porte créée
        mcrea_clients[3] = -1 # Indice d'un mur créé
        
        # Début des tests sur commandes
        # Tests simples d'abord
        print("Début des tests sur quelques commandes simples!")
        
        # Test des commandes de jeu sur le 1er joueur connecté
        # NB : les 3 premiers tests ne sont pas exploités par la suite
        # C'est pour cela que l'on prend une copie de liste_clients[1]
        
        coup = "o1"
        liste, robot, mouvt, pcrea, mcrea, msg, proxy_dep \
            = labyrinthe.modifier_carte(coup, list(liste_clients[1]), robot_clients[1], mouvt_clients[1])
        carte = labyrinthe.formatage_derniere_carte(liste)
        self.assertEqual(pcrea, -1)
        self.assertEqual(mcrea, -1)
        if "Aïe" in msg:
            self.assertEqual(carte_1, carte)
        elif "impossible" in msg:
            self.assertEqual(carte_1, carte)
        else:
            self.assertNotEqual(carte_1, carte)
            
        print("Carte 1 suite coup " + coup + " :\n" + carte + "\n")

        coup = "e1"
        liste, robot, mouvt, pcrea, mcrea, msg, proxy_dep \
            = labyrinthe.modifier_carte(coup, list(liste_clients[1]), robot_clients[1], mouvt_clients[1])
        carte = labyrinthe.formatage_derniere_carte(liste)
        self.assertEqual(pcrea, -1)
        self.assertEqual(mcrea, -1)
        if "Aïe" in msg:
            self.assertEqual(carte_1, carte)
        elif "impossible" in msg:
            self.assertEqual(carte_1, carte)
        else:
            self.assertNotEqual(carte_1, carte)
        
        print("Carte 1 suite coup " + coup + " :\n" + carte + "\n")

        coup = "s1"
        liste, robot, mouvt, pcrea, mcrea, msg, proxy_dep \
            = labyrinthe.modifier_carte(coup, list(liste_clients[1]), robot_clients[1], mouvt_clients[1])
        carte = labyrinthe.formatage_derniere_carte(liste)
        self.assertEqual(pcrea, -1)
        self.assertEqual(mcrea, -1)
        if "Aïe" in msg:
            self.assertEqual(carte_1, carte)
        elif "impossible" in msg:
            self.assertEqual(carte_1, carte)
        else:
            self.assertNotEqual(carte_1, carte)
        
        print("Carte 1 suite coup " + coup + " :\n" + carte + "\n")
            
        coup = "n1"
        
        # Réinitialisation de la place qu'occupait le robot du client 1 chez le 2 & 3
        liste_clients[2][robot_clients[1]] = mouvt_clients[1]
        liste_clients[3][robot_clients[1]] = mouvt_clients[1]
        
        # Modification de la carte du client 1
        indice_X_1 = robot_clients[1]
        liste_clients[1], robot_clients[1], mouvt_clients[1], pcrea_clients[1], mcrea_clients[1], msg, proxy_dep \
            = labyrinthe.modifier_carte(coup, liste_clients[1], robot_clients[1], mouvt_clients[1])
        carte_clients[1] = labyrinthe.formatage_derniere_carte(liste_clients[1])
        self.assertEqual(pcrea_clients[1], -1)
        self.assertEqual(mcrea_clients[1], -1)
        
        print("Carte 1 suite coup " + coup + " :\n" + carte_clients[1] + "\n")
        
        # Tests
        if "Aïe" in msg:
            self.assertEqual(carte_1, carte_clients[1])
        elif "impossible" in msg:
            self.assertEqual(carte_1, carte_clients[1])
        else:
            self.assertNotEqual(carte_1, carte_clients[1])  
            self.assertNotEqual(robot_clients[1], indice_X_1)
            self.assertEqual(liste_clients[1][robot_clients[1]], self.robot)
            
        # Réinitialisation de carte_1
        carte_1 = carte_clients[1]
        
        # Ajout du déplacement du robot du client 1 dans les cartes des clients 2 & 3
        liste_clients[2][robot_clients[1]] = labyrinthe.ajout_robot_adverse(liste_clients[2][robot_clients[1]])
        carte_clients[2] = labyrinthe.formatage_derniere_carte(liste_clients[2])
        
        liste_clients[3][robot_clients[1]] = labyrinthe.ajout_robot_adverse(liste_clients[3][robot_clients[1]])
        carte_clients[3] = labyrinthe.formatage_derniere_carte(liste_clients[3])
        
        print("Carte 2 suite coup " + coup + " :\n" + carte_clients[2] + "\n")
        print("Carte 3 suite coup " + coup + " :\n" + carte_clients[3] + "\n")
        
        # Tests
        if "Aïe" in msg:
            self.assertEqual(carte_2, carte_clients[2])
            self.assertEqual(carte_3, carte_clients[3])
        elif "impossible" in msg:
            self.assertEqual(carte_2, carte_clients[2])
            self.assertEqual(carte_3, carte_clients[3])
        else:
            self.assertNotEqual(carte_2, carte_clients[2])  
            self.assertNotEqual(carte_3, carte_clients[3])
            self.assertEqual(liste_clients[2][robot_clients[1]], self.robot_adverse)
            self.assertEqual(liste_clients[3][robot_clients[1]], self.robot_adverse)
            
        # Réinitialisation de carte_2 & carte_3
        carte_2 = carte_clients[2]
        carte_3 = carte_clients[3]
        
        # Test de la commande "porte" sur client 2 :
        
        # Idem 3 premiers tests non exploités par la suite!
        coup = "po"
        indice_X_2 = robot_clients[2]
        liste, robot, mouvt, pcrea, mcrea, msg, proxy_dep \
            = labyrinthe.modifier_carte(coup, list(liste_clients[2]), robot_clients[2], mouvt_clients[2])
        carte = labyrinthe.formatage_derniere_carte(liste)
        
        print("Carte 2 suite coup " + coup + " :\n" + carte + "\n")
        
        # Tests
        if "impossible" in msg:
            self.assertEqual(robot, indice_X_2)
            self.assertEqual(pcrea, -1)
            self.assertEqual(carte_2, carte)
        elif "empêche" in msg:
            self.assertEqual(robot, indice_X_2)
            self.assertEqual(pcrea, -1)
            self.assertEqual(carte_2, carte)
        elif "créé" in msg:
            self.assertEqual(robot, indice_X_2)
            self.assertNotEqual(pcrea, -1)
            self.assertEqual(liste[pcrea], self.porte)
            self.assertNotEqual(carte_2, carte)
        
        coup = "pe"
        indice_X_2 = robot_clients[2]
        liste, robot, mouvt, pcrea, mcrea, msg, proxy_dep \
            = labyrinthe.modifier_carte(coup, list(liste_clients[2]), robot_clients[2], mouvt_clients[2])
        carte = labyrinthe.formatage_derniere_carte(liste)
        
        print("Carte 2 suite coup " + coup + " :\n" + carte + "\n")
        
        # Tests
        if "impossible" in msg:
            self.assertEqual(robot, indice_X_2)
            self.assertEqual(pcrea, -1)
            self.assertEqual(carte_2, carte)
        elif "empêche" in msg:
            self.assertEqual(robot, indice_X_2)
            self.assertEqual(pcrea, -1)
            self.assertEqual(carte_2, carte)
        elif "créé" in msg:
            self.assertEqual(robot, indice_X_2)
            self.assertNotEqual(pcrea, -1)
            self.assertEqual(liste[pcrea], self.porte)
            self.assertNotEqual(carte_2, carte)
            
        coup = "ps"
        indice_X_2 = robot_clients[2]
        liste, robot, mouvt, pcrea, mcrea, msg, proxy_dep \
            = labyrinthe.modifier_carte(coup, list(liste_clients[2]), robot_clients[2], mouvt_clients[2])
        carte = labyrinthe.formatage_derniere_carte(liste)
        
        print("Carte 2 suite coup " + coup + " :\n" + carte + "\n")
        
        # Tests
        if "impossible" in msg:
            self.assertEqual(robot, indice_X_2)
            self.assertEqual(pcrea, -1)
            self.assertEqual(carte_2, carte)
        elif "empêche" in msg:
            self.assertEqual(robot, indice_X_2)
            self.assertEqual(pcrea, -1)
            self.assertEqual(carte_2, carte)
        elif "créé" in msg:
            self.assertEqual(robot, indice_X_2)
            self.assertNotEqual(pcrea, -1)
            self.assertEqual(liste[pcrea], self.porte)
            self.assertNotEqual(carte_2, carte)
        
        coup = "pn"
        indice_X_2 = robot_clients[2]
        liste_clients[2], robot_clients[2], mouvt_clients[2], pcrea_clients[2], mcrea_clients[2], msg, proxy_dep \
            = labyrinthe.modifier_carte(coup, liste_clients[2], robot_clients[2], mouvt_clients[2])
        carte_clients[2] = labyrinthe.formatage_derniere_carte(liste_clients[2])
        
        print("Carte 2 suite coup " + coup + " :\n" + carte_clients[2] + "\n")
        
        # Tests
        if "impossible" in msg:
            self.assertEqual(robot_clients[2], indice_X_2)
            self.assertEqual(pcrea_clients[2], -1)
            self.assertEqual(carte_2, carte_clients[2])
        elif "empêche" in msg:
            self.assertEqual(robot_clients[2], indice_X_2)
            self.assertEqual(pcrea_clients[2], -1)
            self.assertEqual(carte_2, carte_clients[2])
        elif "créé" in msg:
            self.assertEqual(robot_clients[2], indice_X_2)
            self.assertNotEqual(pcrea_clients[2], -1)
            self.assertEqual(liste_clients[2][pcrea_clients[2]], self.porte)
            self.assertNotEqual(carte_2, carte_clients[2])
            
        # Réinitialisation de carte_2
        carte_2 = carte_clients[2]
        
        # On ajoute la porte aux clients 1 & 3
        if pcrea_clients[2] != -1:
            liste_clients[1][pcrea_clients[2]] = labyrinthe.ajout_porte(liste_clients[1][pcrea_clients[2]])
            carte_clients[1] = labyrinthe.formatage_derniere_carte(liste_clients[1])
            liste_clients[3][pcrea_clients[2]] = labyrinthe.ajout_porte(liste_clients[3][pcrea_clients[2]])
            carte_clients[3] = labyrinthe.formatage_derniere_carte(liste_clients[3])
    
        print("Carte 1 suite coup " + coup + " :\n" + carte_clients[1] + "\n")
        print("Carte 3 suite coup " + coup + " :\n" + carte_clients[3] + "\n")
        
        # Tests
        if "impossible" in msg:
            self.assertEqual(carte_1, carte_clients[1])
            self.assertEqual(carte_3, carte_clients[3])
        elif "empêche" in msg:
            self.assertEqual(carte_1, carte_clients[1])
            self.assertEqual(carte_3, carte_clients[3])
        elif "créé" in msg:
            self.assertNotEqual(carte_1, carte_clients[1])
            self.assertNotEqual(carte_3, carte_clients[3])
            self.assertEqual(liste_clients[1][pcrea_clients[2]], self.porte)
            self.assertEqual(liste_clients[3][pcrea_clients[2]], self.porte)
        
        # Réinitialisation de carte_1 et carte_3
        carte_1 = carte_clients[1]
        carte_3 = carte_clients[3]
        
        # Réinitialisation de pcrea
        pcrea_clients[2] = -1
        
        # Effet mirroir pour client 3 sur mur...
        # Idem 3 premiers tests non exploités par la suite!
        coup = "mo"
        indice_X_3 = robot_clients[3]
        liste, robot, mouvt, pcrea, mcrea, msg, proxy_dep \
            = labyrinthe.modifier_carte(coup, list(liste_clients[3]), robot_clients[3], mouvt_clients[3])
        carte = labyrinthe.formatage_derniere_carte(liste)
        
        print("Carte 3 suite coup " + coup + " :\n" + carte + "\n")
        
        # Tests
        if "impossible" in msg:
            self.assertEqual(robot, indice_X_3)
            self.assertEqual(mcrea, -1)
            self.assertEqual(carte_3, carte)
        elif "empêche" in msg:
            self.assertEqual(robot, indice_X_3)
            self.assertEqual(mcrea, -1)
            self.assertEqual(carte_3, carte)
        elif "créé" in msg:
            self.assertEqual(robot, indice_X_3)
            self.assertNotEqual(mcrea, -1)
            self.assertEqual(liste[mcrea], self.mur)
            self.assertNotEqual(carte_3, carte)
        
        coup = "me"
        indice_X_3 = robot_clients[3]
        liste, robot, mouvt, pcrea, mcrea, msg, proxy_dep \
            = labyrinthe.modifier_carte(coup, list(liste_clients[3]), robot_clients[3], mouvt_clients[3])
        carte = labyrinthe.formatage_derniere_carte(liste)
        
        print("Carte 3 suite coup " + coup + " :\n" + carte + "\n")
        
        # Tests
        if "impossible" in msg:
            self.assertEqual(robot, indice_X_3)
            self.assertEqual(mcrea, -1)
            self.assertEqual(carte_3, carte)
        elif "empêche" in msg:
            self.assertEqual(robot, indice_X_3)
            self.assertEqual(mcrea, -1)
            self.assertEqual(carte_3, carte)
        elif "créé" in msg:
            self.assertEqual(robot, indice_X_3)
            self.assertNotEqual(mcrea, -1)
            self.assertEqual(liste[mcrea], self.mur)
            self.assertNotEqual(carte_3, carte)
            
        coup = "ms"
        indice_X_3 = robot_clients[3]
        liste, robot, mouvt, pcrea, mcrea, msg, proxy_dep \
            = labyrinthe.modifier_carte(coup, list(liste_clients[3]), robot_clients[3], mouvt_clients[3])
        carte = labyrinthe.formatage_derniere_carte(liste)
        
        print("Carte 3 suite coup " + coup + " :\n" + carte + "\n")
        
        # Tests
        if "impossible" in msg:
            self.assertEqual(robot, indice_X_3)
            self.assertEqual(mcrea, -1)
            self.assertEqual(carte_3, carte)
        elif "empêche" in msg:
            self.assertEqual(robot, indice_X_3)
            self.assertEqual(mcrea, -1)
            self.assertEqual(carte_3, carte)
        elif "créé" in msg:
            self.assertEqual(robot, indice_X_3)
            self.assertNotEqual(mcrea, -1)
            self.assertEqual(liste[mcrea], self.mur)
            self.assertNotEqual(carte_3, carte)
        
        coup = "mn"
        indice_X_3 = robot_clients[3]
        liste_clients[3], robot_clients[3], mouvt_clients[3], pcrea_clients[3], mcrea_clients[3], msg, proxy_dep \
            = labyrinthe.modifier_carte(coup, liste_clients[3], robot_clients[3], mouvt_clients[3])
        carte_clients[3] = labyrinthe.formatage_derniere_carte(liste_clients[3])
        
        print("Carte 3 suite coup " + coup + " :\n" + carte_clients[3] + "\n")
        
        # Tests
        if "impossible" in msg:
            self.assertEqual(robot_clients[3], indice_X_3)
            self.assertEqual(mcrea_clients[3], -1)
            self.assertEqual(carte_3, carte_clients[3])
        elif "empêche" in msg:
            self.assertEqual(robot_clients[3], indice_X_3)
            self.assertEqual(mcrea_clients[3], -1)
            self.assertEqual(carte_3, carte_clients[3])
        elif "créé" in msg:
            self.assertEqual(robot_clients[3], indice_X_3)
            self.assertNotEqual(mcrea_clients[3], -1)
            self.assertEqual(liste_clients[3][mcrea_clients[3]], self.mur)
            self.assertNotEqual(carte_3, carte_clients[3])
            
        # Réinitialisation de carte_3
        carte_3 = carte_clients[3]
        
        # On ajoute le mur aux clients 1 & 2
        if mcrea_clients[3] != -1:
            liste_clients[1][mcrea_clients[3]] = labyrinthe.ajout_mur(liste_clients[1][mcrea_clients[3]])
            carte_clients[1] = labyrinthe.formatage_derniere_carte(liste_clients[1])
            liste_clients[2][mcrea_clients[3]] = labyrinthe.ajout_mur(liste_clients[2][mcrea_clients[3]])
            carte_clients[2] = labyrinthe.formatage_derniere_carte(liste_clients[2])
    
        print("Carte 1 suite coup " + coup + " :\n" + carte_clients[1] + "\n")
        print("Carte 2 suite coup " + coup + " :\n" + carte_clients[2] + "\n")
        
        # Tests
        if "impossible" in msg:
            self.assertEqual(carte_1, carte_clients[1])
            self.assertEqual(carte_2, carte_clients[2])
        elif "empêche" in msg:
            self.assertEqual(carte_1, carte_clients[1])
            self.assertEqual(carte_2, carte_clients[2])
        elif "créé" in msg:
            self.assertNotEqual(carte_1, carte_clients[1])
            self.assertNotEqual(carte_2, carte_clients[2])
            self.assertEqual(liste_clients[1][mcrea_clients[3]], self.mur)
            self.assertEqual(liste_clients[2][mcrea_clients[3]], self.mur)
        
        carte_1 = carte_clients[1]
        carte_2 = carte_clients[2]
        
        # Réinitialisation de mcrea
        mcrea_clients[3] = -1
        
        # On fait une boucle et le programme tire au hasard des commandes de jeu
        
        # On crée les commandes de coup que l'on place dans liste_commandes
        # Le nombre de commandes de déplacement dépendent de la taille de liste_1
        liste_commandes = ["o", "e", "s", "n", "po", "pe", "ps", "pn", "mo", "me", "ms", "mn"]
        i = 1
        while i < len(liste_1):
            liste_commandes.append(random.choice(liste_commandes)) # Pour avoir plus de commandes avec porte et mur
            liste_commandes.append(random.choice(liste_commandes)) # Idem
            liste_commandes.append("o" + str(i))
            liste_commandes.append("e" + str(i))
            liste_commandes.append("s" + str(i))
            liste_commandes.append("n" + str(i))
            i += 1
       
        # On fixe le nombre de tirage aléatoire de la boucle (dépend de liste_1)
        nombre_tirage = len(liste_1)*10 # on multiplie par 10 la taille de liste_1
        
        # On lance la boucle
        print("Lancement du test sur commandes aléatoires!\n")
        
        numero_tirage = 1
        while numero_tirage < nombre_tirage:
            coup = random.choice(liste_commandes)
            # On commence par le coup du client 1
            
            # Réinitialisation de la place qu'occupait le robot du client 1 chez le 2 & 3
            liste_clients[2][robot_clients[1]] = mouvt_clients[1]
            liste_clients[3][robot_clients[1]] = mouvt_clients[1]
            
            indice_X_1 = robot_clients[1]
            liste_clients[1], robot_clients[1], mouvt_clients[1], pcrea_clients[1], mcrea_clients[1], msg, proxy_dep \
                = labyrinthe.modifier_carte(coup, liste_clients[1], robot_clients[1], mouvt_clients[1])
            carte_clients[1] = labyrinthe.formatage_derniere_carte(liste_clients[1])
            
            # Tests
            # Cas où l'on sort du jeu tout de suite
            if "impossible" in msg and proxy_dep == 1:
                self.assertEqual(carte_1, carte_clients[1])
            # Autre cas impossible où pas de porte ni de mur à créer
            elif "impossible" in msg and ("p" in coup or "m" in coup):
                self.assertEqual(carte_1, carte_clients[1])
                self.assertEqual(mcrea_clients[1], -1)
                self.assertEqual(pcrea_clients[1], -1)
            # Cas où l'on entre dans un mur ou un robot tout de suite
            elif "Aïe" in msg and proxy_dep == 1:
                self.assertEqual(carte_1, carte_clients[1])
            # Cas où un robot empêche de créer une porte ou un mur
            elif "empêche" in msg:
                self.assertEqual(robot_clients[1], indice_X_1)
                self.assertEqual(mcrea_clients[1], -1)
                self.assertEqual(pcrea_clients[1], -1)
                self.assertEqual(carte_1, carte_clients[1])
            # Cas où l'on crée une porte ou un mur
            elif "créé" in msg:
                self.assertEqual(robot_clients[1], indice_X_1)
                self.assertNotEqual(carte_1, carte_clients[1])
                if "m" in coup:
                    self.assertNotEqual(mcrea_clients[1], -1)
                    self.assertEqual(liste_clients[1][mcrea_clients[1]], self.mur)
                else:
                    self.assertNotEqual(pcrea_clients[1], -1)
                    self.assertEqual(liste_clients[1][pcrea_clients[1]], self.porte)
            # Tous les autres cas avec déplacement donc!
            else:
                self.assertNotEqual(carte_1, carte_clients[1])  
                self.assertNotEqual(robot_clients[1], indice_X_1)
                self.assertEqual(liste_clients[1][robot_clients[1]], self.robot)
            
            # Réinitialisation de carte_1
            carte_1 = carte_clients[1]
            
            # Réinitialisation de pcrea et mcrea
            pcrea_clients[1] = -1
            mcrea_clients[1] = -1
            
            # Ajout du déplacement du robot du client 1 dans les cartes des clients 2 & 3
            liste_clients[2][robot_clients[1]] = labyrinthe.ajout_robot_adverse(liste_clients[2][robot_clients[1]])
            carte_clients[2] = labyrinthe.formatage_derniere_carte(liste_clients[2])
            
            liste_clients[3][robot_clients[1]] = labyrinthe.ajout_robot_adverse(liste_clients[3][robot_clients[1]])
            carte_clients[3] = labyrinthe.formatage_derniere_carte(liste_clients[3])
            
            # Réinitialisation de carte_2 & carte_3
            carte_2 = carte_clients[2]
            carte_3 = carte_clients[3]
            
            # On incrémente numero_tirage
            numero_tirage += 1
            coup = random.choice(liste_commandes)
            
            # On joue avec le client 2
            
            # Réinitialisation de la place qu'occupait le robot du client 2 chez le 1 & 3
            liste_clients[1][robot_clients[2]] = mouvt_clients[2]
            liste_clients[3][robot_clients[2]] = mouvt_clients[2]
            
            indice_X_2 = robot_clients[2]
            liste_clients[2], robot_clients[2], mouvt_clients[2], pcrea_clients[2], mcrea_clients[2], msg, proxy_dep \
                = labyrinthe.modifier_carte(coup, liste_clients[2], robot_clients[2], mouvt_clients[2])
            carte_clients[2] = labyrinthe.formatage_derniere_carte(liste_clients[2])
            
            # Cas où l'on sort du jeu tout de suite
            if "impossible" in msg and proxy_dep == 1:
                self.assertEqual(carte_2, carte_clients[2])
            # Autre cas impossible où pas de porte ni de mur à créer
            elif "impossible" in msg and ("p" in coup or "m" in coup):
                self.assertEqual(carte_2, carte_clients[2])
                self.assertEqual(mcrea_clients[2], -1)
                self.assertEqual(pcrea_clients[2], -1)
            # Cas où l'on entre dans un mur ou un robot tout de suite
            elif "Aïe" in msg and proxy_dep == 1:
                self.assertEqual(carte_2, carte_clients[2])
            # Cas où un robot empêche de créer une porte ou un mur
            elif "empêche" in msg:
                self.assertEqual(robot_clients[2], indice_X_2)
                self.assertEqual(mcrea_clients[2], -1)
                self.assertEqual(pcrea_clients[2], -1)
                self.assertEqual(carte_2, carte_clients[2])
            # Cas où l'on crée une porte ou un mur
            elif "créé" in msg:
                self.assertEqual(robot_clients[2], indice_X_2)
                self.assertNotEqual(carte_2, carte_clients[2])
                if "m" in coup:
                    self.assertNotEqual(mcrea_clients[2], -1)
                    self.assertEqual(liste_clients[2][mcrea_clients[2]], self.mur)
                else:
                    self.assertNotEqual(pcrea_clients[2], -1)
                    self.assertEqual(liste_clients[2][pcrea_clients[2]], self.porte)
            # Tous les autres cas avec déplacement donc!
            else:
                self.assertNotEqual(carte_2, carte_clients[2])  
                self.assertNotEqual(robot_clients[2], indice_X_2)
                self.assertEqual(liste_clients[2][robot_clients[2]], self.robot)
            
            # Réinitialisation de carte_2
            carte_2 = carte_clients[2]
            
            # Réinitialisation de pcrea et mcrea
            pcrea_clients[2] = -1
            mcrea_clients[2] = -1
            
            # Ajout du déplacement du robot du client 2 dans les cartes des clients 1 & 3
            liste_clients[1][robot_clients[2]] = labyrinthe.ajout_robot_adverse(liste_clients[1][robot_clients[2]])
            carte_clients[1] = labyrinthe.formatage_derniere_carte(liste_clients[1])
            
            liste_clients[3][robot_clients[2]] = labyrinthe.ajout_robot_adverse(liste_clients[3][robot_clients[2]])
            carte_clients[3] = labyrinthe.formatage_derniere_carte(liste_clients[3])
            
            # Réinitialisation de carte_1 & carte_3
            carte_1 = carte_clients[1]
            carte_3 = carte_clients[3]
            
            # On incrémente numero_tirage
            numero_tirage += 1
            coup = random.choice(liste_commandes)
            
            # On joue avec le client 3
            
            # Réinitialisation de la place qu'occupait le robot du client 3 chez le 1 & 2
            liste_clients[1][robot_clients[3]] = mouvt_clients[3]
            liste_clients[2][robot_clients[3]] = mouvt_clients[3]
            
            indice_X_3 = robot_clients[3]
            liste_clients[3], robot_clients[3], mouvt_clients[3], pcrea_clients[3], mcrea_clients[3], msg, proxy_dep \
                = labyrinthe.modifier_carte(coup, liste_clients[3], robot_clients[3], mouvt_clients[3])
            carte_clients[3] = labyrinthe.formatage_derniere_carte(liste_clients[3])
        
            # Cas où l'on sort du jeu tout de suite
            if "impossible" in msg and proxy_dep == 1:
                self.assertEqual(carte_3, carte_clients[3])
            # Autre cas impossible où pas de porte ni de mur à créer
            elif "impossible" in msg and ("p" in coup or "m" in coup):
                self.assertEqual(carte_3, carte_clients[3])
                self.assertEqual(mcrea_clients[3], -1)
                self.assertEqual(pcrea_clients[3], -1)
            # Cas où l'on entre dans un mur ou un robot tout de suite
            elif "Aïe" in msg and proxy_dep == 1:
                self.assertEqual(carte_3, carte_clients[3])
            # Cas où un robot empêche de créer une porte ou un mur
            elif "empêche" in msg:
                self.assertEqual(robot_clients[3], indice_X_3)
                self.assertEqual(mcrea_clients[3], -1)
                self.assertEqual(pcrea_clients[3], -1)
                self.assertEqual(carte_3, carte_clients[3])
            # Cas où l'on crée une porte ou un mur
            elif "créé" in msg:
                self.assertEqual(robot_clients[3], indice_X_3)
                self.assertNotEqual(carte_3, carte_clients[3])
                if "m" in coup:
                    self.assertNotEqual(mcrea_clients[3], -1)
                    self.assertEqual(liste_clients[3][mcrea_clients[3]], self.mur)
                else:
                    self.assertNotEqual(pcrea_clients[3], -1)
                    self.assertEqual(liste_clients[3][pcrea_clients[3]], self.porte)
            # Tous les autres cas avec déplacement donc!
            else:
                self.assertNotEqual(carte_3, carte_clients[3])  
                self.assertNotEqual(robot_clients[3], indice_X_3)
                self.assertEqual(liste_clients[3][robot_clients[3]], self.robot)
            
            # Réinitialisation de carte_3
            carte_3 = carte_clients[3]
            
            # Réinitialisation de pcrea et mcrea
            pcrea_clients[3] = -1
            mcrea_clients[3] = -1
            
            # Ajout du déplacement du robot du client 3 dans les cartes des clients 1 & 2
            liste_clients[1][robot_clients[3]] = labyrinthe.ajout_robot_adverse(liste_clients[1][robot_clients[3]])
            carte_clients[1] = labyrinthe.formatage_derniere_carte(liste_clients[1])
            
            liste_clients[2][robot_clients[3]] = labyrinthe.ajout_robot_adverse(liste_clients[2][robot_clients[3]])
            carte_clients[2] = labyrinthe.formatage_derniere_carte(liste_clients[2])
            
            # Réinitialisation de carte_1 & carte_2
            carte_1 = carte_clients[1]
            carte_2 = carte_clients[2]
            
            # On incrémente numero_tirage
            numero_tirage += 1

        print("Test réussi sur " + str(nombre_tirage) + " coups!\n")
        print("La dernière partie du client 1 est \n" + carte_1 + "\n")
        print("La dernière partie du client 2 est \n" + carte_2 + "\n")
        print("La dernière partie du client 3 est \n" + carte_3 + "\n")
        print("Pour rappel : la partie n'a pas été arrêtée en cas de victoire d'un des 3 clients!\n")
        print("Test de la victoire :")
        
        # Je teste la victoire!
        # On lance la même boucle sans limite en nombre de tirage
        # La boucle devra s'arrêter si un des clients trouve la sortie
        
        # Cas où un des robots est déjà sur la sortie
        if mouvt_clients[1] == self.sortie:
            self.assertEqual(labyrinthe.victoire(mouvt_clients[1]), True)
        elif mouvt_clients[2] == self.sortie:
            self.assertEqual(labyrinthe.victoire(mouvt_clients[2]), True)
        elif mouvt_clients[3] == self.sortie:
            self.assertEqual(labyrinthe.victoire(mouvt_clients[3]), True)
        else:
            # Réinitialisation du numéro de tirage
            numero_tirage = 1
            
            sortie_en_recherche = True
            while sortie_en_recherche:
                coup = random.choice(liste_commandes)
                # On commence par le coup du client 1
                
                # Réinitialisation de la place qu'occupait le robot du client 1 chez le 2 & 3
                liste_clients[2][robot_clients[1]] = mouvt_clients[1]
                liste_clients[3][robot_clients[1]] = mouvt_clients[1]
                
                indice_X_1 = robot_clients[1]
                liste_clients[1], robot_clients[1], mouvt_clients[1], pcrea_clients[1], mcrea_clients[1], msg, proxy_dep \
                    = labyrinthe.modifier_carte(coup, liste_clients[1], robot_clients[1], mouvt_clients[1])
                carte_clients[1] = labyrinthe.formatage_derniere_carte(liste_clients[1])
                
                # Tests si sortie
                if "atteinte" in msg:
                    self.assertEqual(mouvt_clients[1], self.sortie)
                    self.assertNotEqual(carte_1, carte_clients[1])
                    self.assertEqual(labyrinthe.victoire(mouvt_clients[1]), True)
                elif "atteinte" in msg:
                    self.assertNotEqual(labyrinthe.victoire(mouvt_clients[1]), True)
                
                # Réinitialisation de carte_1
                carte_1 = carte_clients[1]
                
                # Réinitialisation de pcrea et mcrea
                pcrea_clients[1] = -1
                mcrea_clients[1] = -1
                
                # Ajout du déplacement du robot du client 1 dans les cartes des clients 2 & 3
                liste_clients[2][robot_clients[1]] = labyrinthe.ajout_robot_adverse(liste_clients[2][robot_clients[1]])
                carte_clients[2] = labyrinthe.formatage_derniere_carte(liste_clients[2])
                
                liste_clients[3][robot_clients[1]] = labyrinthe.ajout_robot_adverse(liste_clients[3][robot_clients[1]])
                carte_clients[3] = labyrinthe.formatage_derniere_carte(liste_clients[3])
                
                # Réinitialisation de carte_2 & carte_3
                carte_2 = carte_clients[2]
                carte_3 = carte_clients[3]
                
                if "atteinte" in msg:
                    break
                
                # On incrémente numero_tirage
                numero_tirage += 1
                coup = random.choice(liste_commandes)
                
                # On joue avec le client 2
                
                # Réinitialisation de la place qu'occupait le robot du client 2 chez le 1 & 3
                liste_clients[1][robot_clients[2]] = mouvt_clients[2]
                liste_clients[3][robot_clients[2]] = mouvt_clients[2]
                
                indice_X_2 = robot_clients[2]
                liste_clients[2], robot_clients[2], mouvt_clients[2], pcrea_clients[2], mcrea_clients[2], msg, proxy_dep \
                    = labyrinthe.modifier_carte(coup, liste_clients[2], robot_clients[2], mouvt_clients[2])
                carte_clients[2] = labyrinthe.formatage_derniere_carte(liste_clients[2])
                
                # Tests si sortie
                # Cas où l'on sort du jeu tout de suite
                if "atteinte" in msg:
                    self.assertEqual(mouvt_clients[2], self.sortie)
                    self.assertNotEqual(carte_1, carte_clients[2])
                    self.assertEqual(labyrinthe.victoire(mouvt_clients[2]), True)
                else:
                    self.assertNotEqual(labyrinthe.victoire(mouvt_clients[2]), True)
                
                # Réinitialisation de carte_2
                carte_2 = carte_clients[2]
                
                # Réinitialisation de pcrea et mcrea
                pcrea_clients[2] = -1
                mcrea_clients[2] = -1
                
                # Ajout du déplacement du robot du client 2 dans les cartes des clients 1 & 3
                liste_clients[1][robot_clients[2]] = labyrinthe.ajout_robot_adverse(liste_clients[1][robot_clients[2]])
                carte_clients[1] = labyrinthe.formatage_derniere_carte(liste_clients[1])
                
                liste_clients[3][robot_clients[2]] = labyrinthe.ajout_robot_adverse(liste_clients[3][robot_clients[2]])
                carte_clients[3] = labyrinthe.formatage_derniere_carte(liste_clients[3])
                
                # Réinitialisation de carte_1 & carte_3
                carte_1 = carte_clients[1]
                carte_3 = carte_clients[3]
                
                if "atteinte" in msg:
                    break
                
                # On incrémente numero_tirage
                numero_tirage += 1
                coup = random.choice(liste_commandes)
                
                # On joue avec le client 3
                
                # Réinitialisation de la place qu'occupait le robot du client 3 chez le 1 & 2
                liste_clients[1][robot_clients[3]] = mouvt_clients[3]
                liste_clients[2][robot_clients[3]] = mouvt_clients[3]
                
                indice_X_3 = robot_clients[3]
                liste_clients[3], robot_clients[3], mouvt_clients[3], pcrea_clients[3], mcrea_clients[3], msg, proxy_dep \
                    = labyrinthe.modifier_carte(coup, liste_clients[3], robot_clients[3], mouvt_clients[3])
                carte_clients[3] = labyrinthe.formatage_derniere_carte(liste_clients[3])
            
                 # Tests si sortie
                # Cas où l'on sort du jeu tout de suite
                if "atteinte" in msg:
                    self.assertEqual(mouvt_clients[3], self.sortie)
                    self.assertNotEqual(carte_1, carte_clients[3])
                    self.assertEqual(labyrinthe.victoire(mouvt_clients[3]), True)
                else:
                    self.assertNotEqual(labyrinthe.victoire(mouvt_clients[3]), True)
                
                # Réinitialisation de carte_3
                carte_3 = carte_clients[3]
                
                # Réinitialisation de pcrea et mcrea
                pcrea_clients[3] = -1
                mcrea_clients[3] = -1
                
                # Ajout du déplacement du robot du client 3 dans les cartes des clients 1 & 2
                liste_clients[1][robot_clients[3]] = labyrinthe.ajout_robot_adverse(liste_clients[1][robot_clients[3]])
                carte_clients[1] = labyrinthe.formatage_derniere_carte(liste_clients[1])
                
                liste_clients[2][robot_clients[3]] = labyrinthe.ajout_robot_adverse(liste_clients[2][robot_clients[3]])
                carte_clients[2] = labyrinthe.formatage_derniere_carte(liste_clients[2])
                
                # Réinitialisation de carte_1 & carte_2
                carte_1 = carte_clients[1]
                carte_2 = carte_clients[2]
                
                if "atteinte" in msg:
                    break
                
                # On incrémente numero_tirage
                numero_tirage += 1
            
        print("Sortie atteinte après " + str(numero_tirage) + " coups!\n")
        print("La dernière partie du client 1 est \n" + carte_1 + "\n")
        print("La dernière partie du client 2 est \n" + carte_2 + "\n")
        print("La dernière partie du client 3 est \n" + carte_3 + "\n")

        # Fermeture des connexions
        connexion_avec_serveur_1.close()
        connexion_avec_serveur_2.close()
        connexion_avec_serveur_3.close()

if __name__ == '__main__':
    unittest.main()

