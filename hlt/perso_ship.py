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
                if self.game.game_map[Position(i,j)].halite_amount > new_max and self.game.game_map[Position(i,j)].is_occupied == False:
                    new_max = self.game.game_map[Position(i,j)].halite_amount
                    max_pos = Position(i,j)
        if new_max > max :
           #file.write("Ship {} has target :{}.\n".format(ship.id, max_pos))
            return (max_pos)
        elif val >= self.game.game_map.height / 2:
            return (Calc.detect_closest_worth(self, ship, 1, max / 3 * 2))
        else :
            return (Calc.detect_closest_worth(self, ship, val + 1, max))


    #defini la prochaine position que prendre le ship
    def     get_next_pos(self, ship, objectif) :
        move = self.game.game_map.get_unsafe_moves(ship.position, objectif)
        for direction in move :
            direct = get_correct_dir(ship, direction)
            if direct not in data.planned_pos and not overall.is_enemy(direct) :
                return (direct)
        move = get_best_pos(ship.position, 1, ship, me, game_map)
        return (move)

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


    def    get_best_pos(self, pos, mode, ship) :
        if mode == 1 :
            max = 0
            direction = pos
            for posi in pos.get_surrounding_cardinals() :
                if self.game.game_map[posi].halite_amount >= max \
                and posi not in self.data.planned_pos \
                and posi not in self.data.opp_pos:
                    direction = posi
                    max = self.game.game_map[posi].halite_amount

        else :
            min = self.game.game_map[pos].halite_amount
            direction = pos
            for posi in pos.get_surrounding_cardinals() :
                if self.game.game_map[posi].halite_amount < max \
                and not self.game.game_map[posi].is_occupied \
                and posi not in self.data.opp_pos:
                    direction = posi
                    max = game_map[posi].halite_amount

        return (direction)
