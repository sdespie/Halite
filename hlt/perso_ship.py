import abc
import queue
import hlt
from hlt import constants
from . import commands
from . import *
from .positionals import Direction, Position
from .entity import Entity, Shipyard, Ship, Dropoff
from .positionals import *
from .networking import *
from .perso_ft import *
from .entity import *
from .constants import *
from .game_map import *
import random

class Calc :

    def __init__(self, game, data, me):
        self.game = game
        self.data = data
        self.me = me

    def     detect_closest_worth(self, ship, val, max):
        pos = ship.position
        new_max = max
        for i in range(pos.x - val, pos.x + val):
            for j in range(pos.y - val, pos.y + val):
                if self.game.game_map[Position(i,j)].halite_amount > new_max \
                and self.game.game_map[Position(i,j)].is_occupied == False:
                    new_max = self.game.game_map[Position(i,j)].halite_amount
                    max_pos = Position(i,j)
        if new_max > max :
           #file.write("Ship {} has target :{}.\n".format(ship.id, max_pos))
            return (max_pos)
        elif val >= self.game.game_map.height / 2:
            return (Calc.detect_closest_worth(self, ship, 1, max / 3 * 2))
        else :
            return (Calc.detect_closest_worth(self, ship, val + 1, max))



    # Donne la distance la plus courte etre le ship actuel et le dropoff ou shipyard le plus proche
    def     get_closest_drop_dist(self, ship) :
        min = self.game.game_map.calculate_distance(ship.position, self.me.shipyard.position)
        for dropoff in self.me.get_dropoffs() :
            if min > self.game.game_map.calculate_distance(ship.position, dropoff.position) :
                min = self.game.game_map.calculate_distance(ship.position, dropoff.position)
        return (min)

    # donne la position du dropoff ou shipyard le plus proche d'un ship
    def     get_closest_drop_pos(self, ship) :
        min = self.game.game_map.calculate_distance(ship.position, self.me.shipyard.position)
        pos = self.me.shipyard.position
        for dropoff in self.me.get_dropoffs() :
            if min > self.game.game_map.calculate_distance(ship.position, dropoff.position) :
                min = self.game.game_map.calculate_distance(ship.position, dropoff.position)
                pos = dropoff.position
        return (pos)


        '''
        J'ai reduit un peu cette merde
        '''

    def    get_best_pos(self, pos, ship) :
        max = 0
        direction = pos
        for posi in pos.get_surrounding_cardinals() :
            if self.game.game_map[posi].halite_amount >= max \
            and posi not in self.data.planned_pos \
            and posi not in self.data.opp_pos:
                direction = posi
                max = self.game.game_map[posi].halite_amount
        return (direction)


    '''
    J'ai essayer de faire une nouvelle fonction pour les mouvements en exploration.
    Je prend d'abord la liste des get_unsafe_moves (max 2 output, dans la direction)
    et regarde combien sont encore valide par rapport au zone deja utilise
    Si il n'y a qu'un choix, je le prend, si il en a deux, je prend le mieux: soit >100 pour miner,
    soit le minimum pour limiter la consommation
    Sinon, je regardes autour ou je peux aller (mais j'ai pas encore fait cette partie la, et je suis fatigué)
    '''

    def next_pos_exploring(self, ship, destination, overall):
        move = self.game.game_map.get_unsafe_moves(ship.position, destination)
        for dest in move :
            if overall.get_correct_dir(ship.position, dest) in self.data.planned_dest \
            or overall.get_correct_dir(ship.position, dest) in self.data.opp_pos :
                move.remove(dest)
        if len(move) == 1 :
            return (move[0])
        elif len(move) == 2 :
            move1 = self.game.game_map[overall.get_correct_dir(ship.position, move[1])].halite_amount
            move0 = self.game.game_map[overall.get_correct_dir(ship.position, move[0])].halite_amount
            if move1 > move0 :
                if move1 >= 100 :
                    return (move[1])
                else :
                    return (move[0])
            else :
                if move0 >= 100 :
                    return (move[0])
                else :
                    return (move[1])
        #else :
