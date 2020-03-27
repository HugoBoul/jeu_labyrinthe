# -*- coding: utf-8 -*
import os
from labyrinthe import *
	
def choix_carte(liste, chemin):
	#choix de la carte par rapport à la liste des fichiers cartes recensés dans répertoires facile ou prison dans le cas où aucune partie en cours
	#au préalable vérifier qu'il n'y a pas qu'une seule carte!
	if len(liste) > 1:
		print("Vous avez {} choix de labyrinthes".format(len(liste)))
		choix_en_cours = True
		while choix_en_cours == True:
			#le joueur sélectionne un numéro pour faire afficher les cartes : entre 1 et le nombre de cartes présentes
			message = "Saisisser un numéro de labyrinthe parmi ceux disponibles - un numéro entre 1 et " + repr(len(liste)) + " : "
			choix = input(message)
			if not choix.isnumeric() or int(choix) > len(liste):
				print("Merci de saisir un choix valide!")
			else:
				#ce numéro est utilisé pour faire afficher la carte
				fichier_labyrinthe = liste[int(choix)-1]
				os.chdir(chemin)
				mon_fichier = open(fichier_labyrinthe, "r")
				ma_carte = mon_fichier.read()
				mon_fichier.close()
				print(ma_carte)
				print()
				#le joueur a encore le choix d'accepter ou pas la carte sélectionnée
				validation = input("Ok pour ce labyrinthe o/n? : ")
				validation = validation.lower()
				while validation != "o" and validation != "n":
					validation = input("Ok pour ce labyrinthe o/n? : ")
				if validation == "o":
					choix_en_cours = False
	else:
		choix = 0
		fichier_labyrinthe = liste[choix]
		os.chdir(chemin)
		mon_fichier = open(fichier_labyrinthe, "r")
		ma_carte = mon_fichier.read()
		mon_fichier.close()
	return ma_carte

		
