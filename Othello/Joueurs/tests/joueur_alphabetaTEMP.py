#-*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

#coef [1,-2]
coef = [0, 0, 100]
caseVal = [[100, -20, 10, 5, 5, 10, -20, 100],
           [-20, -50, -2, -2, -2, -2, -50, -20],
           [10, -2, -1, -1, -1, -1, -2, 10],
           [5, -2, -1, -1, -1, -1, -2, 5],
           [5, -2, -1, -1, -1, -1, -2, 5],
           [10, -2, -1, -1, -1, -1, -2, 10],
           [-20, -50, -2, -2, -2, -2, -50, -20],
           [100, -20, 10, 5, 5, 10, -20, 100]]
depth = 1
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
    """ jeu*coup -> double
        retourne le 'poids' du coup passé en argument, calculé à partir
        de la somme des coef_i*f_i, où coef_i est définit en variable globale et
        f_i differentes fonctions
    """

    return coef[0]*getValCase(jeu,joueur) +\
    coef[1]*getCoupsOfferts(jeu, joueur)  +\
    coef[2]*getLiberte(jeu,joueur)

def getValCase(jeu,joueur):
    res=0
    for i in range(8):
        for j in range(8):
            if(jeu[0][i][j]==joueur):
                res+=caseVal[i][j]
    return res

def getLiberte(jeu,joueur):
    nb=0
    for i in range(8):
        for j in range(8):
            if(jeu[0][i][j]==joueur):
                d=0
                for di in range(-1,2):
                    for dj in range (-1,2):
                        if i+di < 8 and i+di >= 0 and j+dj < 8 and dj+j >=0:
                            if jeu[0][i+di][j+dj] == 0:
                                d+=1
                if(d<=5):
                    nb+=1
    return nb


def getScore(jeuAv,jeuAp, joueur):
    return jeuAp[4][joueur-1]-jeuAv[4][joueur-1]

def getCoupsOfferts(jeu, joueur):
    if jeu[1]==joueur:
        return len(game.getCoupsValides(jeu))
    else:
        return -len(game.getCoupsValides(jeu))

def getNbCoupsJoueur(jeu,joueur):
    coupsValides = game.getCoupsValides(jeu)
    m = -100
    for c in coupsValides:
        m = max(m,caseVal[c[0]][c[1]])

    if jeu[1]==joueur:
        return m
    else :
        return -m

def getCoupsOfferts2(jeu,joueur):
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
        return 0

    for c in l:
        #on evalue la valeur de ses coups
        res -= caseVal[c[0]][c[1]]

    #on renvoie la valeur d'un coup moyen
    #peut etre pas ouf a tester avec la valeur max
    return res*1.0/nbCoup


def getFinPartie(jeu,joueur):
    g=game.getGagnant(jeu)
    if(g==joueur):
        return 1000
    elif (g==0):
        return -100
    else:
        return -1000
