#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
sys.path.append("..")
import game

def initialiseJeu():
    """ void -> jeu
    	Initialise le jeu pour l'othello
    	Hypothese: le plateau fera toujours 8*8 cases vides
        avec 4 jetons alternés au milieu
    """
    jeu = []
    plateau = [[0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,2,1,0,0,0],
               [0,0,0,1,2,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0]]

    jeu.append(plateau)
    jeu.append(1);
    jeu.append(None)
    jeu.append([[3,3],[4,3],[3,4],[4,4]])
    jeu.append([2,2])
    return jeu

def getCoupsValides(jeu):
    """ jeu -> List[coup]
        Retourne la liste des coups valides dans le jeu
    	c-a-d le liste des coups qui 'enjambent' une suite de pions de l'adversaire
    """
    res = []
    plateau = jeu[0]
    #on parcours toutes les cases du plateau
    for i in range (8):
        for j in range (8):
            boolBreak = False
            #si c'est une case nulle, on regarde toutes les cases autour
            if plateau[i][j] == 0:
                for di in range (-1, 2):
                    for dj in range (-1, 2):
                        #(i,j) est valide si elle enjambe des pieces adverses
                        if estValide(jeu, i, j, di, dj):
                            #alors on l'ajoute à la liste des coups valides
                            res.append([i,j])
                            boolBreak = True
                            break
                    if boolBreak :
                        break
    return res

def finJeu(jeu):
    """ jeu -> bool
        renvoie true si le jeu est fini, false sinon.
        Hypothèse: le jeu se finit forcèment quand il n'y a plus de coups valides
        au maximum il y aura 64 (8x8 cases) itérations du jeu
    """
    if game.getCoupsValides(jeu)==[]:
        return True
    return False

def finalise(jeu):
    """ jeu -> void
        Met a jour les scores finaux des joueurs quand la partie est terminee
    """
    sc1 = 0
    sc2 = 0
    #on regarde toutes les cases du plateau et ajoute les pions aux scores des joueurs
    for i in range (8):
	for j in range (8):
	    if jeu[0][i][j]==1:
                sc1+=1
	    elif jeu[0][i][j]==2:
                sc2+=1
    jeu[4][0] = sc1
    jeu[4][1] = sc2

def estValide(jeu, i, j, di ,dj):
    """ jeu*int*int*int*int -> bool
        renvoie vrai si ya une case a elle dans la direction dx dy
        Hypothèse: Il faut au moins un pion de l'adversaire entre
    """
    adversaire = jeu[1]%2+1
    i+=di
    j+=dj
    #on regarde déjà si la case d après est un adversaire ou non (sinon c'est sûr c'est pas un coup valide)
    if (i < 8 and i >= 0 and j < 8 and j >= 0 and jeu[0][i][j] != adversaire):
        return False
    #ensuite on parcours toutes les cases jusqu'a la limite du tableaun jusqu'à tomber
    #sur un pion du joueur ou sur une case vide
    while (i < 8 and i >= 0 and j < 8 and j >= 0):
        if jeu[0][i][j] == jeu[1]:
            return True
        if jeu[0][i][j] == 0:
            return False
        i += di
        j += dj
    return False

def poserPiece(jeu, i, j, di, dj):
    """ jeu*int*int*int*int -> void
        pose/retourne les pieces pour le joueur courant
    """
    adversaire = jeu[1]%2+1
    jeu[0][i][j] = jeu[1]
    i+=di
    j+=dj
    score = 0
    #on parcours toute la ligne/colonne/diagonnale et on pose/retourne les pieces pour le joueur courant
    while (i >= 0 and i< 8 and j >= 0 and j<8 and jeu[0][i][j]==adversaire):
        jeu[0][i][j] = jeu[1]
        i+=di
        j+=dj
        score +=1
    
    jeu[4][jeu[1]-1]+=score
    jeu[4][jeu[1]%2]-=score

def joueCoup(jeu,coup):
    """ jeu*coup -> void
        joue le coup choisi par le joueur
    """
    #pose toutes les pieces dans toutes les directions engendrées par le coup joué
    jeu[4][jeu[1] - 1] += 1    
    for di in range (-1, 2):
        for dj in range (-1, 2):
            if estValide(jeu, coup[0], coup[1], di, dj):
                poserPiece(jeu, coup[0], coup[1], di, dj)


def copie(jeu):
    return [[[jeu[0][i][j] for j in range(8)] for i in range(8)]
            ,jeu[1],None,[e for e in jeu[3]],[jeu[4][0],jeu[4][1]]]
