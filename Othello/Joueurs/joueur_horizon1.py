#-*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game
import copy
import random

coef = [1, 1000]
caseVal = [[100, -20, 10, 5, 5, 10, -20, 100],
           [-20, -50, -2, -2, -2, -2, -50, -20],
           [10, -2, -1, -1, -1, -1, -2, 10],
           [5, -2, -1, -1, -1, -1, -2, 5],
           [5, -2, -1, -1, -1, -1, -2, 5],
           [10, -2, -1, -1, -1, -1, -2, 10],
           [-20, -50, -2, -2, -2, -2, -50, -20],
           [100, -20, 10, 5, 5, 10, -20, 100]]

def saisieCoup(jeu):
    """ jeu -> coup
        retourne le coup choisi par décision
    """
    return decision(jeu)

def decision(jeu):
    """ jeu -> coup
        retourne le coup qui a le score le plus élevé pour une itération du jeu
        Hypothèse: si tous les coups on le même score, alors on joue le premier coup valide
    """
    listeCoups = game.getCoupsValides(jeu)
    res = listeCoups[0]
    listeCoups.remove(res)
    maxRes = estimation(jeu,res)
    for c in listeCoups:
        score = estimation(jeu,c)
        if(score>maxRes):
            maxRes=score
            res=c
    return res

def estimation(jeu,coup):
    """ jeu*coup -> double
        retourne l'évaluation du coup passé en paramètre. (en horizon 1 uniquement)
    """
    return evaluation(jeu,coup)

def evaluation(jeu, coup):
    """ jeu*coup -> double
        retourne le 'poids' du coup passé en argument, calculé à partir
        de la somme des coef_i*f_i, où coef_i est définit en variable globale et
        f_i differentes fonctions
    """
    joueurCourant = jeu[1]
    jeuSave = game.getCopieJeu(jeu)
    game.joueCoup(jeuSave, coup)

    return coef[0]*getCoupsOfferts(jeuSave,joueurCourant) + \
    coef[1]*getFinPartie(jeuSave, joueurCourant)


def getValCase(jeu,joueur):
    res=0
    for i in range(8):
        for j in range(8):
            if(jeu[0][i][j]==joueur):
                res+=caseVal[i][j]
            elif(jeu[0][i][j]==joueur%2+1):
                res-=caseVal[i][j]
    return res

def getCoupsOfferts(jeu,joueur):
    #on triche si c'est pas a lui de jouer
    #du coup pas sur que la fonction soit utile
    #quand c'est pas a l'adversaire de jouer
    jeu[1]=joueur%2 +1
    res=0
    l=game.getCoupsValides(jeu)
    nbCoup = len(l)
    if(nbCoup==0):
        #s'il n'a pas de coup possible on renvoie le score de fin de game
        #peut etre que c'est pareil si on renvoie 0
        return coef[1]*getFinPartie(jeu, joueur)

    for c in l:
        #on evalue la valeur de ses coups
        res -= caseVal[c[0]][c[1]]

    #on renvoie la valeur d'un coup moyen
    #peut etre pas ouf a tester avec la valeur max
    return res*1.0/nbCoup


def getFinPartie(jeu, joueur):
    """ jeu*int -> int
        retourne la valeur de fin de partie (1=gagné, -1=perdu, 0=pas finit)
    """
    if game.finJeu(jeu):
        g=game.getGagnant(jeu)
        if(g==joueur):
            return 1
        elif(g==0):
            return -0.1
        else:
            return -1
    else:
        return 0
