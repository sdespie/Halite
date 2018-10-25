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
