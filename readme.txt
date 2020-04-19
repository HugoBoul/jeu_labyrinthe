Mécanisme :
- lancement via le fichier serveur.py
- ensuite choix d'un labyrinthe
- ensuite lancement du jeu en ouvrant le fichier client.py (autant de fois que l'on veut de joueur)

- rappel de l'objectif : chaque joueur est un robot "X". Les robots adverses sont représentés par "x". L'objectif est de gagner la sortie "U" avec le robot
Les symboles du jeu : "O" est un mur (il bloque le robot), "." est une porte (le robot peut passer par là)

- ensuite commandes de jeu à passer :
-- "C" pour commencer la partie (il faut au moins 2 joueurs connectés)
-- "e + nombre de pas" : pour déplacement à l'Est (e2 : le robot se déplace à l'Est de 2 pas)
-- "o", "n", et "s" même principe pour déplacements à l'Ouest, au Nord et au Sud
-- "m" + "e" ou "o" ou "n" ou "s" pour créer un mur dans les sens indiqués
-- "p" + "e" ou "o" ou "n" ou "s" pour créer une porte dans les sens indiqués

Le fichier fonctions.py comprend les fonctions utilisées par le programme

Le fichier labyrinthe.py comprend la classe du labyrinthe

Le dossier carte comprend les labyrinthes que l'on peut utiliser

Le fichier test.py permet de tester que le programme fonctionne bien

Pour toutes questions/remarques, merci de contacter Hugo Boulanger
