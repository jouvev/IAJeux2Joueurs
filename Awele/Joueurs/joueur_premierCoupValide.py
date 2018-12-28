# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """ 
    if jeu[1]==1:
        case = 0
        sens = 1
    elif jeu[1]==2:
        case = 5
        sens = -1
    
    while True:
        coup = [jeu[1]-1,case]
        if coup in game.getCoupsValides(jeu):
            return coup
        case+=sens