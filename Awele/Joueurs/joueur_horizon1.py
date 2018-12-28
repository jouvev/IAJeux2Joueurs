#-*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game
import copy

coef = [2, -1, 0, 0, 100]

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
    res = premierCoup(jeu)
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

def evaluation(jeu,coup):
    """ jeu*coup -> double
        retourne le 'poids' du coup passé en argument, calculé à partir
        de la somme des coef_i*f_i, où coef_i est définit en variable globale et
        f_i differentes fonctions
    """
    joueurCourant = jeu[1]
    jeuSave = game.getCopieJeu(jeu)
    game.joueCoup(jeuSave, coup)
    return coef[0]*(getScore(jeuSave,joueurCourant)-jeu[4][joueurCourant-1]) + \
    coef[1]*getCasesSuccesives(jeuSave,joueurCourant) + \
    coef[2]*getNbGraines(jeuSave, joueurCourant) + \
    coef[3]*getPlusDePossibilite(jeuSave,joueurCourant) + \
    coef[4]*getFinPartie(jeuSave,joueurCourant)

def getScore(jeu, joueur):
    """ jeu*int -> int
        retourne le score d'un joueur
    """
    return jeu[4][joueur-1]

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

def getNbGraines(jeu, joueur):
    nbJoueur=0
    nbAdversaire=0
    adversaire = joueur%2
    for i in range (6):
        nbJoueur += jeu[0][joueur-1][i]
        nbAdversaire += jeu[0][adversaire][i]
    return nbJoueur-nbAdversaire

def getPlusDePossibilite(jeu,joueur):
    toucherCouler = [0,0,0,0,0,0]
    for i in range(6):
        val = jeu[0][joueur-1][i]
        nbG = ((val//12)+val)%12
        if (joueur-1==0):
            nbG-=i
        else:
            nbG-=(5-i)
        if(nbG>0 and nbG<=6):
            toucherCouler[nbG-1]+=1
    res = 0
    for e in toucherCouler:
        if(e>0):
            res+=1
    return res

def getFinPartie(jeu,joueur):
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

def premierCoup(jeu):
    """ jeu -> coup
        retourne le premier coup valide
    """
    if jeu[1]==1:
        case = 5
        sens = -1
    else:
        case = 0
        sens = 1
    while True:
        coup = [jeu[1]-1,case]
        if coup in game.getCoupsValides(jeu):
            return coup
        case+=sens
