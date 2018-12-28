#!/usr/bin/env python
#-*- coding: utf-8 -*-
import copy

# plateau: List[List[nat]]
# liste de listes (lignes du plateau) d'entiers correspondant aux contenus des cases du plateau de jeu

# coup: Pair[nat nat]
# Numero de ligne et numero de colonne de la case correspondante a un coup d'un joueur

# Jeu
# jeu:N-UPLET[plateau nat List[coup] List[coup] Pair[nat nat]]
# Structure de jeu comportant :
#           - le plateau de jeu
#           - Le joueur a qui c'est le tour de jouer (1 ou 2)
#           - La liste des coups possibles pour le joueur a qui c'est le tour de jouer
#           - La liste des coups joues jusqu'a present dans le jeu
#           - Une paire de scores correspondant au score du joueur 1 et du score du joueur 2

game=None #Contient le module du jeu specifique: awele ou othello
joueur1=None #Contient le module du joueur 1
joueur2=None #Contient le module du joueur 2


#Fonctions minimales

def getCopieJeu(jeu):
    """ jeu -> jeu
        Retourne une copie du jeu passe en parametre
        Quand on copie un jeu on en calcule forcement les coups valides avant
    """
    return game.copie(jeu)

def finJeu(jeu):
    """ jeu -> bool
        Retourne vrai si c'est la fin du jeu
    """
    return game.finJeu(jeu)

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
        On suppose que la fonction n'est appelee que si il y a au moins un coup valide possible
        et qu'elle retourne obligatoirement un coup valide
    """
    if getJoueur(jeu)==1:
    	return joueur1.saisieCoup(jeu)
    else:
    	return joueur2.saisieCoup(jeu)

def joueCoup(jeu,coup):
    """ jeu*coup -> void
        Joue un coup a l'aide de la fonction joueCoup defini dans le module game
        Hypothese:le coup est valide
        Met tous les champs de jeu à jour (sauf coups valides qui est fixée à None)
    """
    game.joueCoup(jeu,coup)#update le plateau et le score
    changeJoueur(jeu)
    jeu[2]=None
    jeu[3].append(coup)


def initialiseJeu():
    """ void -> jeu
        Initialise le jeu (nouveau plateau, liste des coups joues vide, liste des coups valides None, scores a 0 et joueur = 1)
    """
    return game.initialiseJeu()

def getGagnant(jeu):
    """ jeu -> nat
    	Retourne le numero du joueur gagnant apres avoir finalise la partie. Retourne 0 si match nul
    """
    game.finalise(jeu)
    score1 = getScore(jeu,1)
    score2 = getScore(jeu,2)
    if score1>score2:
        return 1
    elif score2>score1:
        return 2
    else:
        return 0

def affiche(jeu):
    """ jeu -> void
        Affiche l'etat du jeu de la maniere suivante :
                 Coup joue = <dernier coup>
                 Scores = <score 1>, <score 2>
                 Plateau :

                         |       0     |     1       |      2     |      ...
                    ------------------------------------------------
                      0  | <Case 0,0>  | <Case 0,1>  | <Case 0,2> |      ...
                    ------------------------------------------------
                      1  | <Case 1,0>  | <Case 1,1>  | <Case 1,2> |      ...
                    ------------------------------------------------
                    ...       ...          ...            ...
                 Joueur <joueur>, a vous de jouer

         Hypothese : le contenu de chaque case ne depasse pas 5 caracteres
    """
    s=""
    nbLignes = len(jeu[0])
    if(nbLignes != 0):
        nbColonnes = len(jeu[0][0])
    s+= "".center(5," ")+"|"
    for j in range(0,nbColonnes):
        s+= str(j).center(5," ")+"|"
    nb=len(s)
    s+= "\n"+"-"*(nb)+"\n"
    for i in range (0, nbLignes):
        s+= str(i).center(5," ")+"|"
        for j in range (0, nbColonnes):
            s+= str(jeu[0][i][j]).center(5," ")+"|"
        s+= "\n"+"-"*(nb)+"\n"
    print s


# Fonctions utiles

def getPlateau(jeu):
    """ jeu -> plateau
        Retourne le plateau du jeu passe en parametre
    """
    return jeu[0]

def getCoupsJoues(jeu):
    """ jeu -> List[coup]
        Retourne la liste des coups joues dans le jeu passe en parametre
    """
    return jeu[3]

def getCoupsValides(jeu):
    """ jeu -> List[coup]
        Retourne la liste des coups valides dans le jeu passe en parametre
        Si None, alors on met à jour la liste des coups valides
    """
    if jeu[2] is None:
    	jeu[2]=game.getCoupsValides(jeu)
    return jeu[2]

def getScores(jeu):
    """ jeu -> Pair[nat nat]
        Retourne les scores du jeu passe en parametre
    """
    return jeu[4]

def getJoueur(jeu):
    """ jeu -> nat
        Retourne le joueur a qui c'est le tour de jouer dans le jeu passe en parametre
    """
    return jeu[1]

def changeJoueur(jeu):
    """ jeu -> void
        Change le joueur a qui c'est le tour de jouer dans le jeu passe en parametre (1 ou 2)
    """
    if jeu[1] == 1:
        jeu[1] = 2
    else:
        jeu[1] = 1

def getScore(jeu, joueur):
    """ jeu*nat -> int
        Retourne le score du joueur
        Hypothese: le joueur est 1 ou 2
    """
    return jeu[4][joueur-1]

def getCaseVal(jeu, ligne, colonne):
    """ jeu*nat*nat -> nat
        Retourne le contenu de la case ligne,colonne du jeu
        Hypothese: les numeros de ligne et colonne appartiennent bien au plateau  : ligne<=getNbLignes(jeu) and colonne<=getNbColonnes(jeu)
    """
    return jeu[0][ligne][colonne]
