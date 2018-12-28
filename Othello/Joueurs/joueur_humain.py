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
        i = input("saisir ligne entre 0 et 7:")
        j = input("saisir colonne entre 0 et 7:")
        coup = [i,j]
        if coup in game.getCoupsValides(jeu) :
            break
        print("Coups invalide!!!!!!!!!!!!")
    return coup
