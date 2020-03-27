#-*- coding: utf-8 _*
import random

class Labyrinthe():
    mur = "O"
    porte = "."
    sortie = "U"
    robot = "X"
    robot_adverse = "x"
    vide = " "
    taille_ligne = 0
    nombre_joueur_max = 0
    
    def __init__(self, numero_client):
        self.nb_robot = numero_client
    
    def nombre_joueur_maximum(self, carte):
        """ calcul du nombre de joueur maximum """
        liste = [] # Initialisation de l'indexation de carte dans cette liste
        liste_vide = [] # Initialisation de la liste des vides
        compteur = 0
        for symbole_carte in carte:
        # Calcul du nombre de joueur maximum
            if symbole_carte == self.vide or symbole_carte == self.mur or symbole_carte == self.porte or \
                symbole_carte == self.robot or symbole_carte == self.sortie:
                liste.append(symbole_carte)
                compteur += 1
            if liste[compteur-1] == self.vide:
                liste_vide.append(compteur-1)
        self.nombre_joueur_max = len(liste_vide)
        return self.nombre_joueur_max
    
    def creation_derniere_carte(self, carte):
        """ ajout du nouveau joueur (indice_X) dans une carte indexée en liste """
        liste = [] # Initialisation de l'indexation de carte dans cette liste
        liste_vide = [] # Initialisation de la liste des vides
        premier_passage = True
        compteur = 0
        indice_X = self.vide
        if self.nb_robot > 1:
            carte = carte.replace(self.robot, self.robot.lower())
        for symbole_carte in carte:
        # Récupération des symboles
            if symbole_carte == self.vide or symbole_carte == self.mur or symbole_carte == self.porte or \
                symbole_carte == self.robot.lower() or symbole_carte == self.robot or \
                    symbole_carte == self.sortie:
                liste.append(symbole_carte)
                compteur += 1
            else:
                if premier_passage == True:
                # Récupération de la taille d'une ligne
                    self.taille_ligne = len(liste)
                    premier_passage = False
            if liste[compteur-1] == self.vide:
                liste_vide.append(compteur-1)
        # Création du nouveau robot
        indice_X = random.choice(liste_vide)
        liste[indice_X] = self.robot
        return liste, indice_X
        
    def formatage_derniere_carte(self, liste):
        """ formatage d'une carte indexée """
        #ajouter un saut de ligne avec taille_ligne
        compteur = 0
        compteur_retour_ligne = 1
        nouvelle_carte = ""
        for symbole_carte in liste:
            compteur += 1
            nouvelle_carte += symbole_carte
            if compteur == compteur_retour_ligne * self.taille_ligne and compteur != len(liste):# Le dernier contrôle sert à ne pas ajouter le dernier espace
                nouvelle_carte += "\n"
                compteur_retour_ligne += 1
        return nouvelle_carte
                
    def ajout_robot_adverse(self, liste_elt):
        liste_elt = self.robot_adverse
        return liste_elt
                            
    def ajout_porte(self, liste_elt):
        liste_elt = self.porte
        return liste_elt
                    
    def ajout_mur(self, liste_elt):
        liste_elt = self.mur
        return liste_elt
            
    def victoire(self, liste_elt):
        victoire = False
        if liste_elt == self.sortie:
            victoire = True
        return victoire
    
    def modifier_carte(self, coup, liste, indice_X, mouvt):
        """ modifier carte gère les commandes clients, les modifications sont indexées """
        position_robot = indice_X
        pas = "" # Intialisation du déplacement de la commande de jeu
        # Ajout des pas de la commande de jeu s'ils sont implicites
        if len(coup) == 1:
            pas = 1
        elif "m" in coup or "p" in coup:
            pas = len(liste)
        else:
            pas = int(coup[1:])
        
        # Initialisation des variables nouvelle porte / nouveau mur
        indice_porte = -1
        indice_mur = -1
        
        deplacement = 1 # On fera prendre à déplacement toutes les valeurs entières jusque "pas"
        msg = "" # Intialisation du commentaire à envoyer au joueur suite à sa commande de jeu
        
        # On boucle jusqu'à pas
        # Par contre la boucle peut-être interrompu avant si obstacle ou sortie de la carte par exemple
        while deplacement - 1 < pas:
        
            # Déplacement en fonction des directions cardinales
            if "n" in coup:
                indice_robot = indice_X-self.taille_ligne*deplacement
            if "s" in coup:
                indice_robot = indice_X+self.taille_ligne*deplacement
            if "o" in coup:
                indice_robot = indice_X-deplacement
            if "e" in coup:
                indice_robot = indice_X+deplacement
            
            # Création du msg de jeu pour le joueur
            
            # Cas des coups impossibles
            if (deplacement > self.taille_ligne-indice_X%self.taille_ligne-1 and "e" in coup) or \
                (deplacement > indice_X%self.taille_ligne and "o" in coup):
                if "m" and "p" not in coup:
                    msg = "Coup impossible : sortie de jeu!"
                    break
                elif "m" in coup:
                    msg = "Coup impossible: pas de mur à créer!"
                    break
                else:
                    msg = "Coup impossible: pas de porte à créer!"
                    break
            if indice_robot < 0 or indice_robot > len(liste)-1:
                if "m" and "p" not in coup:
                    msg = "Coup impossible : sortie de jeu!"
                    break
                elif "m" in coup:
                    msg = "Coup impossible: pas de mur à créer!"
                    break
                else:
                    msg = "Coup impossible: pas de porte à créer!"
                    break
            if liste[indice_robot] == self.mur and "m" in coup:
                msg = "Coup impossible : pas de porte à murer!"
                break
            if liste[indice_robot] == self.sortie and "m" in coup:
                msg = "Coup impossible : la sortie ne peut pas être murée!"
                break
            if liste[indice_robot] == self.sortie and "p" in coup:
                msg = "Coup impossible : pas de porte à la sortie!"
                break
            
            # Cas des portes et murs créés
            if liste[indice_robot] == self.mur and "p" in coup:
                msg = "J'ai créé une porte!"
                break
            if liste[indice_robot] == self.porte and "m" in coup:
                msg = "J'ai créé un mur!"
                break
            
            # Cas des rencontres avec un robot adverse
            if liste[indice_robot] == self.robot_adverse and ("m" and "p" not in coup):
                msg = "Aïe, je me suis pris un robot!"
                break
            if liste[indice_robot] == self.robot_adverse and "m" in coup:
                msg = "Un robot m'empêche de créer un mur!"
                break
            if liste[indice_robot] == self.robot_adverse and "p" in coup:
                msg = "Un robot m'empêche de créer une porte!"
                break
            
            # Cas d'un déplacement du robot
            if liste[indice_robot] == self.mur and "m" not in coup:
                msg = "Aïe, je me suis pris un mur!"
                break
            if liste[indice_robot] == self.sortie and ("m" and "p" not in coup):
                position_robot = indice_robot
                msg = "Sortie atteinte!" # on affichera le message final de victoire avec Labyrinthe.victoire
                break 
            
            # On incrémente déplacement et on actualise la position du robot :
            deplacement += 1
            position_robot = indice_robot
            
            # Si l'on ne sort pas de la boucle le msg est le suivant :
            msg = "Je déplace le robot"
        
        if msg == "Je déplace le robot" or msg == "Aïe, je me suis pris un mur!" or msg == "Aïe, je me suis pris un robot!" or \
            msg == "Coup impossible : sortie de jeu!" or msg == "Sortie atteinte!":
            liste[indice_X] = mouvt # On reinitialise l'origine ancienne du robot (porte ou vide)
            mouvt = liste[position_robot] # On garde en mémoire l'origne nouvelle du robot
            liste[position_robot] = self.robot # On place le robot sur non nouvel emplacement
        
        elif msg == "J'ai créé une porte!":
            liste[indice_robot] = self.porte # On crée la nouvelle porte
            indice_porte = indice_robot # On garde en mémoire l'emplacement de la nouvelle porte
            position_robot = indice_X # On replace la position du robot à l'origine (pas de déplacement)
        
        elif msg == "J'ai créé un mur!":
            liste[indice_robot] = self.mur # On crée le nouveau mur
            indice_mur = indice_robot # On garde en mémoire l'emplacement du nouveau mur
            position_robot = indice_X # On replace la position du robot à l'origine (pas de déplacement)
        
        else:
            position_robot = indice_X # On replace la position du robot à l'origine (pas de déplacement)
        
        return liste, position_robot, mouvt, indice_porte, indice_mur, msg, deplacement
            
            
        
            
            
        
    
        
    
        
        
        
            
        
