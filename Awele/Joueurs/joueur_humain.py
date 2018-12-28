# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    #rajout du while(true) avec break , qui fait office de do_while
    while(True):
        case = input("saisir une case entre 0 et 5:")
        coup = [game.getJoueur(jeu)-1,case]
        if coup in game.getCoupsValides(jeu) :
            break
        print("Coups invalide!!!!!!!!!!!!")
    return coup
