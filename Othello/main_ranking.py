#!/usr/bin/env python
#-*- coding: utf-8 -*-
import random
import othello
import sys
sys.path.append("..")
import game
game.game=othello

sys.path.append("./Joueurs")
import joueur_alphabeta
import joueur_minmax
import joueur_horizon1
import joueur_premierCoupValide
import joueur_random
import joueur_humain
import joueur_alphabetaEleve

oracle=joueur_alphabeta
eleve=joueur_alphabetaEleve
game.joueur1=eleve
game.joueur2=joueur_minmax


def joue():
    """ void -> int
        fonction qui lance une partie du jeu avec les deux joueurs définit
        Hypothèse: on fait 4 tours de placements aléatoires au début pour
        améliorer les résultats.
        Le jeu se finit forcément.
    """
    jeu=game.initialiseJeu()
    i=0

    while (i < 4):
        coup = joueur_random.saisieCoup(game.getCopieJeu(jeu))
        game.joueCoup(jeu,coup)
        i+=1
    while(not game.finJeu(jeu)):
        #print "joueur:",jeu[1]
        #print "score 1:",jeu[4][0]," score 2:",jeu[4][1]
        #game.affiche(jeu)
        if(jeu[1]==1):
            ranking(jeu)
        coup = game.saisieCoup(game.getCopieJeu(jeu))
        game.joueCoup(jeu,coup)
    gagnant = game.getGagnant(jeu)
    print eleve.coef
    return gagnant

def joueN(n):
    victoires=[0,0,0]
    for i in range(n//2):
        g=joue()
        victoires[g] += 1
    #on switch les joueurs
    j = game.joueur2
    game.joueur2 = game.joueur1
    game.joueur1 = j
    for i in range(n//2):
        g=joue()
        if g==1:
            g=2
        elif g==2:
            g=1
        victoires[g] += 1
    return victoires

def ranking(jeu,alpha=0.01):
    params=eleve.coef
    listeCoups=game.getCoupsValides(jeu)
    o=[oracle.estimation(jeu,c,oracle.depth,jeu[1],-5000,5000) for c in listeCoups]
    opt=oracle.decision(jeu)
    saveJeu = game.getCopieJeu(jeu)
    game.joueCoup(saveJeu, opt)
    scrOpt=eleve.evals(saveJeu,jeu[1])
    sOpt=oracle.dot(eleve.coef,scrOpt)
    for i in range(len(listeCoups)):
        if(o[i]<o[listeCoups.index(opt)]):
            saveJeu = game.getCopieJeu(jeu)
            game.joueCoup(saveJeu, listeCoups[i])
            scrO=eleve.evals(saveJeu,jeu[1])
            sO=oracle.dot(eleve.coef,scrO)
            if (sOpt-sO)<1:
                for j in range(len(params)):
                    params[j]=params[j]-alpha*(scrO[j]-scrOpt[j])



joueN(1000)
