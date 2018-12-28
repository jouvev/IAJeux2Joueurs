#-*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

coef = [0.25, 1, 0.25]
#1 +- 0.5
#1.25
caseVal = [[10.0, -2.0, 1.0, 0.5, 0.5, 1.0, -2.0, 10.0],
           [-2.0, -5.0, -0.2, -0.2, -0.2, -0.2, -5.0, -2.0],
           [1.0, -0.2, -0.1, -0.1, -0.1, -0.1, -0.2, 1.0],
           [0.5, -0.2, -0.1, -0.1, -0.1, -0.1, -0.2, 0.5],
           [0.5, -0.2, -0.1, -0.1, -0.1, -0.1, -0.2, 0.5],
           [1.0, -0.2, -0.1, -0.1, -0.1, -0.1, -0.2, 1.0],
           [-2.0, -5.0, -0.2, -0.2, -0.2, -0.2, -5.0, -2.0],
           [10.0, -2.0, 1.0, 0.5, 0.5, 1.0, -2.0, 10.0]]
depth = 3
MAX=5000
MIN=-5000

def saisieCoup(jeu):
    return decision(jeu)

def decision(jeu):
    listeCoups = game.getCoupsValides(jeu)
    trimax(listeCoups)
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

def estimation(jeu, profondeur, joueur,alpha,beta):
    if (game.finJeu(jeu)):
        g=game.getGagnant(jeu)
        if(g==joueur):
            return 1000
        elif (g==0):
            return -100
        else:
            return -1000

    if (profondeur == 0):
        return evaluation(jeu, joueur)

    listeCoups = game.getCoupsValides(jeu)
    if(joueur == jeu[1]):
        trimax(listeCoups)
        #max
        val = MIN
        for c in listeCoups:
            saveJeu = game.getCopieJeu(jeu)
            game.joueCoup(saveJeu, c)
            val = max(val, estimation(saveJeu, profondeur-1, joueur,alpha,beta))
            if(beta <= val):
                return val
            alpha = max(alpha, val)
        return val
    else:
        trimin(listeCoups)
        #min
        val = MAX
        for c in listeCoups:
            saveJeu = game.getCopieJeu(jeu)
            game.joueCoup(saveJeu, c)
            val = min(val, estimation(saveJeu, profondeur-1, joueur,alpha,beta))
            if(alpha >= val):
                return val
            beta = min(beta, val)
        return val

def evaluation(jeu, joueur):
    simpleParcours=parite_getCaseVal(jeu, joueur)
    return coef[0]*simpleParcours[0] + \
    coef[1]*simpleParcours[1] + \
    coef[2]*mobilite(jeu, joueur)
    
    

def parite_getCaseVal(jeu, joueur):
    joueurTotal=0
    adversaireTotal=0
    getValCase=0
    for i in range(8):
        for j in range(8):
            if(jeu[0][i][j]==joueur):
                joueurTotal+=1
                getValCase+=caseVal[i][j]
            elif(jeu[0][i][j]==joueur%2+1):
                adversaireTotal+=1
                getValCase-=caseVal[i][j]
    return [joueurTotal-adversaireTotal, getValCase]

def mobilite(jeu, joueur):
    mobilite_courante=len(game.getCoupsValides(jeu))
    jeu[2]=None
    adversaire=joueur%2+1
    jeu[1]=adversaire
    if jeu[1]!=joueur:
        return mobilite_courante-len(game.getCoupsValides(jeu))
    else:
        return len(game.getCoupsValides(jeu))-mobilite_courante
        
def trimax(liste):
    imax=0
    
    vmax=caseVal[liste[0][0]][liste[0][1]]
    for i in range(1,len(liste)):
        v=caseVal[liste[i][0]][liste[i][1]]
        if v>vmax:
            imax=i
            vmax=v
    
    tmp=liste[0]
    liste[0]=liste[imax]
    liste[imax]=tmp            
                      
def trimin(liste):
    imax=0
    
    vmax=caseVal[liste[0][0]][liste[0][1]]
    for i in range(1,len(liste)):
        v=caseVal[liste[i][0]][liste[i][1]]
        if v<vmax:
            imax=i
            vmax=v
    
    tmp=liste[0]
    liste[0]=liste[imax]
    liste[imax]=tmp   