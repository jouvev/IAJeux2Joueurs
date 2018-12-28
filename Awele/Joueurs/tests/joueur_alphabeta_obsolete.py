#-*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

coef = [2, -1, 1, 1000]
depth = 3
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
    if jeu[1] == 2:
        listeCoups.reverse()
    maxVal = MIN
    maxCoup = None
    for c in listeCoups:
        saveJeu = game.getCopieJeu(jeu)
        game.joueCoup(saveJeu, c)
        val = estimation(saveJeu, depth-1, jeu[1],MIN,MAX)
        if(val>maxVal):
            maxVal = val
            maxCoup = c
    return maxCoup

def estimation(jeu, profondeur, joueur, alpha, beta):
    if (profondeur == 0 or game.finJeu(jeu)):
        return evaluation(jeu, joueur)
    #listeCoups = game.getCoupsValides(jeu)
    listeCoups = updateListe(jeu, game.getCoupsValides(jeu))
    if(joueur == jeu[1]):
        #max
        maxVal = MIN
        for c in listeCoups:
            saveJeu = game.getCopieJeu(jeu)
            game.joueCoup(saveJeu, c)
            val = estimation(saveJeu, profondeur-1, joueur, alpha, beta)
            maxVal = max (val, maxVal)
            if(beta <= maxVal):
                return maxVal
            alpha = max(alpha,maxVal)
        return maxVal
    else:
        #min
        minVal = MAX
        #listeCoups.reverse()
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
    coef[2]*getCasesSuccesives(jeu,joueur%2 + 1) + \
    coef[3]*getFinPartie(jeu,joueur)

def getScore(jeu, joueur):
    """ jeu*int -> int
        retourne le score d'un joueur
    """
    adversaire = joueur%2 + 1
    return jeu[4][joueur-1] - jeu[4][adversaire-1]

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
        if(case==0 or case==1 or case==2):
            nb+=1
        else:
            nbmax=max(nb,nbmax)
            nb=0
    nbmax=max(nb,nbmax)
    return nbmax

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


def updateListe(jeu, listeCoups):
    """ pour chaque coup: on prend son nb de graine, le ramène à modulo 12,
        le colle à la case la plus proche du camp adverse. si le nbG obtenu est
        entre 1 et 6(compri) alors le coup finira dans le camp adverse.

        on renvoi la liste triée avec le plus de graines possibles qui finissent
        dans le camps adverse.
        dans l'ordre : 6->1->le reste
    """
    res = []
    res2 = []
    for c in listeCoups:
        val = jeu[0][c[0]][c[1]]
        nbG = ((val//12)+val)%12
        if (c[0]==0):
            nbG-=c[1]
        else:
            nbG-=(5-c[1])
        res.append((nbG, c))

    #fonction de tri par rapport à la première valeur de chaque tuple, plus grandes valeurs au debut
    res = sorted(res, key=getKey, reverse=True)
    size = len(res)
    i = 0
    #comme 6 est la plus grande valeur souhaitable
    #(et on peut avoir des valeurs jusqu'à 11, alors on met les valeurs >6 à la fin)
    while i<size:
        if res[0][0]>6 or res[0][0]<=0:
            res.append(res[0])
            res.pop(0)
        else:
            break
        i+=1
    for (value, coup) in res:
        res2.append(coup)
    return res2

def getKey(item):
    return item[0]
