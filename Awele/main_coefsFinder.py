#!/usr/bin/env python
#-*- coding: utf-8 -*-
import random
import awele
import sys
sys.path.append("..")
import game
game.game=awele

sys.path.append("./Joueurs")
import joueur_alphabeta
import joueur_minmax
import joueur_horizon1
import joueur_premierCoupValide
import joueur_random
import joueur_humain

game.joueur1=joueur_alphabeta
game.joueur2=joueur_minmax

nbgame=50


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
        coup = game.saisieCoup(game.getCopieJeu(jeu))
        game.joueCoup(jeu,coup)
    gagnant = game.getGagnant(jeu)
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

def train(eps=0.5,n=100):#decay=0.999
    params=game.joueur1.coef
    while True:
        for j in range(len(params)):
            v1=joueN(n)[1]#joue n parties
            x=random.random()
            if(x<0.5):
                m=-eps
            else:
                m=eps
            params[j]+=m
            v2=joueN(n)[1]
            if(v1>v2):
                params[j]-=m
            print (v2, params)

train()
