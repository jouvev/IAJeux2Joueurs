#-*- coding: utf-8 -*-

import sys
sys.path.append("../..")
import game

coef = [2,-1,1000,1]
#profondeur de la simuation
profondeurGlobal = 3

def saisieCoup(jeu):
    """ jeu -> coup
    """
    maxVal=-5000
    
    #pour tous les coups
    listeCoups=game.getCoupsValides(jeu)
    for coup in listeCoups:

        #on save le jeu
        jeuSave=copie(jeu)
        #simule le coup
        game.joueCoup(jeuSave,coup)
        
        val = fonctionMin(jeuSave,jeu[1],profondeurGlobal)
        if(val > maxVal):
            maxVal=val
            meilleurCoup = coup

    #on joue vraiment le meilleur coup
    return meilleurCoup
        
        
    
def fonctionMin(jeu,joueur,profondeur):
    if(game.finJeu(jeu) or profondeur == 0):
        #on evalue le jeu en l'état
        return evaluation(jeu,joueur)

    #sinon on va plus loin dans la simulation
    minVal=5000
    
    listeCoups=game.getCoupsValides(jeu)
    for coup in listeCoups:

        #on save le jeu
        jeuSave=copie(jeu)
        #simule le coup
        game.joueCoup(jeuSave,coup)
        
        val = fonctionMax(jeuSave,joueur,profondeur-1)
        if(val < minVal):
            minVal=val

        #on annule le coup
        #jeu=jeuSave

    #on joue vraiment le meilleur coup
    return minVal
    
        
def fonctionMax(jeu,joueur,profondeur):
    if(game.finJeu(jeu) or profondeur == 0):
        #on evalue le jeu en l'état
        return evaluation(jeu,joueur)

    #sinon on va plus loin dans la simulation
    maxVal=-5000
    
    listeCoups=game.getCoupsValides(jeu)
    for coup in listeCoups:

        #on save le jeu
        jeuSave=copie(jeu)
        #simule le coup
        game.joueCoup(jeuSave,coup)
        
        val = fonctionMin(jeuSave,joueur,profondeur-1)
        if(val > maxVal):
            maxVal=val

    #on joue vraiment le meilleur coup
    return maxVal
    
def evaluation(jeu,joueur):
    return coef[0]*getScore(jeu,joueur) + \
        coef[1]*getCasesSuccesives(jeu,joueur) +\
        coef[2]*getFinPartie(jeu,joueur)+\
        coef[3]*getCasesSuccesives(jeu,joueur%2+1) 

def getScore(jeu, joueur):
    """faire des test sur cette fonction"""
    return jeu[4][joueur-1]-jeu[4][joueur%2]

def getCasesSuccesives(jeu,joueur):
    nb=0
    nbmax=0    
    for i in range(6):
        case = jeu[0][joueur-1][i]
        if(case == 0 or case==1 or case==2):
            nb+=1
        else:
            nbmax=max(nb,nbmax)
            nb=0

    nbmax=max(nb,nbmax)
    return nbmax

def getFinPartie(jeu,joueur):
    if game.finJeu(jeu):
        if(game.getGagnant(jeu)==joueur):
            return 1
        else:
            return -1
    else:
        return 0

def copie(jeu):
    return [[[jeu[0][i][j] for j in range(6)] for i in range(2)]
            ,jeu[1],[],[],[jeu[4][0],jeu[4][1]]]
