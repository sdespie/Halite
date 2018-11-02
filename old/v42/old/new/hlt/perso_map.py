import abc
import queue
import hlt
from hlt import constants
from . import commands
from . import *
from . positionals import *
from . entity import *
from . networking import *
from . perso_constants import *
from . entity import *
from . constants import *
from . game_map import *
import random

class Map :

    def __init__(self, game, data, me):
        self.game = game
        self.data = data
        self.me = me

    def analyse_map (self):
        for i in range(0, self.game.game_map.height - 1) :
            for j in range (0, self.game.game_map.height - 1) :
                if self.game.game_map[Position(i, j)].ship \
                and self.me.has_ship(self.game.game_map[Position(i, j)].ship.id) == False :
                    self.data.opp_pos.append(self.game.game_map.normalize(Position(i + 0, j + 0)))
                    self.data.opp_pos.append(self.game.game_map.normalize(Position(i - 1, j + 0)))
                    self.data.opp_pos.append(self.game.game_map.normalize(Position(i + 1, j + 0)))
                    self.data.opp_pos.append(self.game.game_map.normalize(Position(i + 0, j - 1)))
                    self.data.opp_pos.append(self.game.game_map.normalize(Position(i + 0, j + 1)))


        self.data.max_radar = (-200 * self.game.turn_number / constants.MAX_TURNS + 400) * 2 / self.data.nbr_player
        self.data.max_turn_to_base = 0;
        self.data.nbr_turn_left = constants.MAX_TURNS - self.game.turn_number
