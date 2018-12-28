# -*- coding: utf-8 -*-
import sys
import random
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer aleatoire
    """
    return random.choice(game.getCoupsValides(jeu))
