# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

coef = [1]
caseVal = [[100, -20, 10, 5, 5, 10, -20, 100],
           [-20, -50, -2, -2, -2, -2, -50, -20],
           [10, -2, -1, -1, -1, -1, -2, 10],
           [5, -2, -1, -1, -1, -1, -2, 5],
           [5, -2, -1, -1, -1, -1, -2, 5],
           [10, -2, -1, -1, -1, -1, -2, 10],
           [-20, -50, -2, -2, -2, -2, -50, -20],
           [100, -20, 10, 5, 5, 10, -20, 100]]
depth = 2
MAX=5000
MIN=-5000

def saisieCoup(jeu):
    """ jeu -> coup
        retourne le coup choisi par décision
    """
    if (len(game.getCoupsValides(jeu))==1):
        return game.getCoupsValides(jeu)[0]
    else:
        return decision(jeu)

def decision(jeu):
    """ jeu -> coup
        retourne le coup qui a le score le plus élevé pour une itération du jeu
        Hypothèse: si tous les coups on le même score, alors on joue le premier coup valide
    """
    listeCoups = game.getCoupsValides(jeu)
    maxVal = MIN
    maxCoup = None
    alpha=MIN
    beta=MAX
    for c in listeCoups:
        val = estimation(jeu, c, depth-1, jeu[1],alpha,beta)
        if(val>maxVal):
            maxVal = val
            maxCoup = c
        alpha=max(maxVal,alpha)
    return maxCoup

def estimation(jeu, coup, profondeur, joueur, alpha, beta):
    saveJeu = game.getCopieJeu(jeu)
    game.joueCoup(saveJeu, coup)
    if(game.finJeu(saveJeu)):
        return getFinPartie(saveJeu,joueur)
    if (profondeur == 0):
        return evaluation(saveJeu,joueur)
    listeCoups = game.getCoupsValides(saveJeu)
    if(joueur == saveJeu[1]):
        #max
        maxVal = MIN
        for c in listeCoups:
            val = estimation(saveJeu, c, profondeur-1, joueur,alpha,beta)
            maxVal = max (val, maxVal)
            if(beta <= maxVal):
                return maxVal
            alpha = max(alpha,maxVal)
        return maxVal
    else:
        #min
        minVal = MAX
        for c in listeCoups:
            val = estimation(saveJeu, c, profondeur-1, joueur,alpha,beta)
            minVal= min (val, minVal)
            if(alpha >= minVal):
                return minVal
            beta = min(beta,minVal)
        return minVal


def dot(l1,l2):
    res=0
    for i in range(len(l1)):
        res+=l1[i]*l2[i]
    return res

def evals(jeu, joueur):
    return [getCoupsOfferts(jeu,joueur)]

def evaluation(jeu, joueur):
    return dot(evals(jeu,joueur),coef)


def getCoupsOfferts(jeu,joueur):
    #on triche si c'est pas a lui de jouer
    #du coup pas sur que la fonction soit utile
    #quand c'est pas a l'adversaire de jouer
    jeu[1]=joueur%2 +1
    res=0
    l=game.getCoupsValides(jeu)
    jeu[1]=joueur
    nbCoup = len(l)
    if(nbCoup==0):
        #s'il n'a pas de coup possible on renvoie le score de fin de game
        #peut etre que c'est pareil si on renvoie 0
        return getFinPartie(jeu, joueur)
    for c in l:
        #on evalue la valeur de ses coups
        res -= caseVal[c[0]][c[1]]
    #on renvoie la valeur d'un coup moyen
    #peut etre pas ouf a tester avec la valeur max
    return res*1.0/nbCoup


def getFinPartie(jeu, joueur):
    g=game.getGagnant(jeu)
    if(g==joueur):
        return 1000
    elif (g==0):
        return -100
    else:
        return -1000


# def getValCase(jeu,joueur):
#     res=0
#     for i in range(8):
#         for j in range(8):
#             if(jeu[0][i][j]==joueur):
#                 res+=caseVal[i][j]
#             elif(jeu[0][i][j]==joueur%2+1):
#                 res-=caseVal[i][j]
#     return res
