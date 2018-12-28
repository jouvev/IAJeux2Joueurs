#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
sys.path.append("..")
import game

def initialiseJeu():
    """ void -> jeu
    	Initialise le jeu pour l'awele
    	Hypothese: le plateau fera toujours 2*6 cases remplies de 4 à l'initialisation
    """
    jeu = []
    plateau = [[4,4,4,4,4,4],[4,4,4,4,4,4]]
    jeu.append(plateau)
    jeu.append(1);
    jeu.append([[0,0],[0,1],[0,2],[0,3],[0,4],[0,5]])
    jeu.append([])
    jeu.append([0,0])
    return jeu

def getCoupsValides(jeu):
    """ jeu -> List[coup]
        Retourne la liste des coups valides dans le jeu
    	c-a-d le liste des coups dont les trous n'ont pas 0 graines et qui n'affament pas l'adversaire
    """
    joueur = game.getJoueur(jeu)
    adversaire = joueur%2 +1
    adversaireAffame = estAffame(jeu, adversaire)
    listeCoup=[]

    for case in range(0,6):
        #si l'adversaire est affame
        if adversaireAffame:
            #si le coup permet de rajouter des graines chez l'adversaire alors c'est un coup valide
            if joueur==2 and jeu[0][joueur-1][case] > 5-case:
                 listeCoup.append([joueur-1,case])
            elif joueur==1 and jeu[0][joueur-1][case] > case:
                listeCoup.append([joueur-1,case])
        #sinon, si le trou du joueur n'est pas vide, c'est un coup valide
        elif jeu[0][joueur-1][case]!=0:
            listeCoup.append([joueur-1,case])
    return listeCoup

def finJeu(jeu):
    """ jeu -> bool
        renvoie true si le jeu est fini, false sinon.
    """
    if(len(jeu[3])>=100):
        return True
    if (len(game.getCoupsValides(jeu))==0):
        return True
    if (jeu[4][0] >= 25 or jeu[4][1] >= 25):
        return True
    return False

def finalise(jeu):
    """ jeu -> void
        Met a jour les scores finaux des joueurs quand la partie est terminee
    """
    sc1 = game.getScore(jeu, 1)
    sc2 = game.getScore(jeu, 2)

    for i in range (0, len(jeu[0])):
        sc1 += jeu[0][0][i]
        sc2 += jeu[0][1][i]
    jeu[4][0] = sc1
    jeu[4][1] = sc2

def estAffame(jeu, joueur):
    """ jeu*int -> bool
        Retourne true si le joueur en parametre est affame, false sinon.
    	on est affame lorsque tout son plateau (au joueur) vaut 0
    """
    for i in range (0, 6):
        if jeu[0][joueur-1][i] != 0:
            return False
    return True

def egrainer(jeu,coup):
    """ jeu*coup -> void
        Met a jour le plateau en egrainant les graines du trou selectionne
    """
    coupCourant = [coup[0],coup[1]]
    nbGraines = jeu[0][coup[0]][coup[1]]
    jeu[0][coup[0]][coup[1]] = 0

    while(nbGraines > 0):
        coupCourant = getNextCase(jeu,coupCourant)
        if coupCourant != coup:
            jeu[0][coupCourant[0]][coupCourant[1]]+=1
            nbGraines-=1
    return coupCourant

def getNextCase(jeu,c):
    """ jeu*coup -> coup
        renvoie le coup/case suivante en fonction du joueur
        Si on est le joueur 1 à la case 0, on change le joueur
        Si on est le joueur 2 à la case 5, on change le joueur
    """
    if c[0]==0:
        if c[1]==0 :
            return [1,0]
        else :
            return [0,c[1]-1]
    else :
        if c[1]==5:
            return [0,5]
        else:
            return [1,c[1]+1]

def joueCoup(jeu,coup):
    """ jeu*coup -> void
        joue le coup choisi par le joueur, met à jour le plateau et les scores
        Hypothese: on ne compte pas les scores si l'adversaire est affame
    """
    coupCourant = egrainer(jeu,coup)
    saveJeu = game.getCopieJeu(jeu)

    #si on finit d egrainer dans notre camp, inutile de compter les points
    #sinon (on a finit d'egrainer dans les cases de l'adversaire) il faut les compter en revenant en arriere
    if coup[0]!=coupCourant[0]:
        #pour revenir en arriere on a besoin du sens et de la limite en fonction du coté du plateau
        if coupCourant[0]+1 == 1 :
            sens = 1
            limite = 6
        else :
            sens = -1
            limite = -1
        #ensuite on parcours le plateau dans le sens, jusqu'à attendre la limite definie avant
        #tant qu'on a des cases 'mangeable' (avec 2 ou 3 graines)
        while (coupCourant[1] - limite != 0 and
            saveJeu[0][coupCourant[0]][coupCourant[1]] >=2 and
            saveJeu[0][coupCourant[0]][coupCourant[1]] <= 3):
                #on prend les graines mangées et les ajoute au score, puis met le trou à 0
                saveJeu[4][coup[0]] += saveJeu[0][coupCourant[0]][coupCourant[1]]
                saveJeu[0][coupCourant[0]][coupCourant[1]]=0
                #case suivante
                coupCourant[1]+=sens
        #on regarde si, après comptabilisation des scores, l'adversaire est affamé
        #et si non, on aplique le nouveau plateau/score au jeu actuel
        if not estAffame(saveJeu, coupCourant[0]+1):
            jeu[0]=saveJeu[0]
            jeu[4][coup[0]]= saveJeu[4][coup[0]]

def copie(jeu):
    return [[[jeu[0][i][j] for j in range(6)] for i in range(2)]
            ,jeu[1],None,[e for e in jeu[3]],[jeu[4][0],jeu[4][1]]]
