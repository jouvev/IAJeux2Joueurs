#-*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game
import copy
import random

coef = [1, -1, 1000]
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
    listeCoup = game.getCoupsValides(jeu)
    res = listeCoup[0]
    listeCoup.remove(res)
    maxRes = estimation(jeu,res)
    for c in listeCoup:
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

    return coef[0]*caseVal[coup[0]][coup[1]] +\
    coef[1]*getCoupsOfferts(jeuSave) + \
    coef[2]*getFinPartie(jeuSave, joueurCourant)


def getScore(jeuAv,jeuAp, joueur):
    return jeuAp[4][joueur-1]-jeuAv[4][joueur-1]
    
def getCoupsOfferts(jeu):
    return len(game.getCoupsValides(jeu))

def getFinPartie(jeu, joueur):
    """ jeu*int -> int
        retourne la valeur de fin de partie (1=gagné, -1=perdu, 0=pas finit)
    """
    if game.finJeu(jeu):
        if(game.getGagnant(jeu)==joueur):
            return 1
        else:
            return -1
    else:
        return 0
