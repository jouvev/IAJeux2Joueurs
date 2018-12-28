# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    listeCoups = game.getCoupsValides(jeu)
    return listeCoups[0]
