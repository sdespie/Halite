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
import logging

class Perso:

    def __init__(self, game):
        self.game = game

    def get_players_nbr(self, data):
        for i in range(0, self.game.game_map.height - 1) :
            for j in range (0, self.game.game_map.height - 1) :
                if self.game.game_map[Position(i, j)].has_structure :
                    data.nbr_player += 1

    def analyse_map (self, me, data):
        for i in range(0, self.game.game_map.height - 1) :
            for j in range (0, self.game.game_map.height - 1) :
                if self.game.game_map[Position(i, j)].ship and me.has_ship(self.game.game_map[Position(i, j)].ship.id) == False :
                    data.opp_pos.append(self.get_correct_dir(Position(i, j), (0, 0)))
                    data.opp_pos.append(self.get_correct_dir(Position(i, j), (-1, 0)))
                    data.opp_pos.append(self.get_correct_dir(Position(i, j), (1, 0)))
                    data.opp_pos.append(self.get_correct_dir(Position(i, j), (0, -10)))
                    data.opp_pos.append(self.get_correct_dir(Position(i, j), (0, 1)))

        data.max_radar = (-200 * self.game.turn_number / constants.MAX_TURNS + 400) * 2 / data.nbr_player
        data.max_turn_to_base = 0;
        data.nbr_turn_left = constants.MAX_TURNS - self.game.turn_number


    def     get_correct_dir(self, position, direction) :
        if position.x + direction[0] < 0:
            x = self.game.game_map.height - 1
        elif position.x + direction[0] >= self.game.game_map.height :
            x = 0
        else :
            x = position.x + direction[0]

        if position.y + direction[1] < 0:
            y = self.game.game_map.height - 1
        elif position.y + direction[1] >= self.game.game_map.height :
            y = 0
        else :
            y = position.y + direction[1]
        return (Position(x, y))
