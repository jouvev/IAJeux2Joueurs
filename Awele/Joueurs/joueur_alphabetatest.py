#-*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

coef = [2,-1,1]
depth = 6
MAX=5000
MIN=-5000

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
    
    if jeu[1]==2:
        listeCoups.reverse()
        
    maxVal = MIN
    maxCoup = None
    alpha=MIN
    beta=MAX
    for c in listeCoups:
        saveJeu = game.getCopieJeu(jeu)
        game.joueCoup(saveJeu, c)
        val = estimation(saveJeu, depth-1, jeu[1],alpha,beta)
        if(val>maxVal):
            maxVal = val
            maxCoup = c
        alpha=max(maxVal,alpha)
    return maxCoup


def estimation(jeu, profondeur, joueur, alpha, beta):
    if(game.finJeu(jeu)):
        return getFinPartie(jeu,joueur)

    if (profondeur == 0):
        return evaluation(jeu,joueur)

    listeCoups = game.getCoupsValides(jeu)

    if(joueur == jeu[1]):
        #max
        maxVal = MIN

        for c in listeCoups:
            saveJeu = game.getCopieJeu(jeu)
            game.joueCoup(saveJeu, c)
            val = estimation(saveJeu, profondeur-1, joueur,alpha,beta)
            maxVal = max (val, maxVal)
            if(beta <= maxVal):
                return maxVal
            alpha = max(alpha,maxVal)
        return maxVal
    else:
        #min
        minVal = MAX

        for c in listeCoups:
            saveJeu = game.getCopieJeu(jeu)
            game.joueCoup(saveJeu, c)
            val = estimation(saveJeu, profondeur-1, joueur,alpha,beta)
            minVal= min (val, minVal)
            if(alpha >= minVal):
                return minVal
            beta = min(beta,minVal)

        return minVal


def evaluation(jeu, joueur):
    return coef[0]*getScore(jeu,joueur) + \
    coef[1]*getCasesSuccesives(jeu,joueur) + \
    coef[2]*getCasesSuccesives(jeu,joueur%2 + 1)


def getScore(jeu, joueur):
    """ jeu*int -> int
        retourne le score d'un joueur
    """
    return jeu[4][joueur-1]-jeu[4][joueur%2]

def getCasesSuccesives(jeu,joueur):
    """ jeu*int -> int
        retourne le nombre maximum de cases successives valant 2 ou 3.
        Hypothèse: c'est désavantageux d'avoir des cases faibles
        car l'adversaire peut les manger au tour suivant.
        le coef devra donc être negatif
    """
    nb=0
    nbmax=0
    for i in range(6):
        case = jeu[0][joueur-1][i]
        if(case ==0 or case==1 or case==2):
            nb+=1
        else:
            nbmax=max(nb,nbmax)
            nb=0
    nbmax=max(nb,nbmax)
    return nbmax

def getFinPartie(jeu,joueur):
    g=game.getGagnant(jeu)
    if(g==joueur):
        return 1000
    elif (g==0):
        return -100
    else:
        return -1000
