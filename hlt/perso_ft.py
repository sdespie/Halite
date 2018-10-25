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

class Overall:

    def __init__(self, game, data, me):
        self.game = game
        self.data = data
        self.me = me

    def get_players_nbr(self):
        for i in range(0, self.game.game_map.height - 1) :
            for j in range (0, self.game.game_map.height - 1) :
                if self.game.game_map[Position(i, j)].has_structure :
                    self.data.nbr_player += 1

    def analyse_map (self):
        for i in range(0, self.game.game_map.height - 1) :
            for j in range (0, self.game.game_map.height - 1) :
                if self.game.game_map[Position(i, j)].ship and self.me.has_ship(self.game.game_map[Position(i, j)].ship.id) == False :
                    self.data.opp_pos.append(self.get_correct_dir(Position(i, j), (0, 0)))
                    self.data.opp_pos.append(self.get_correct_dir(Position(i, j), (-1, 0)))
                    self.data.opp_pos.append(self.get_correct_dir(Position(i, j), (1, 0)))
                    self.data.opp_pos.append(self.get_correct_dir(Position(i, j), (0, -10)))
                    self.data.opp_pos.append(self.get_correct_dir(Position(i, j), (0, 1)))

        self.data.max_radar = (-200 * self.game.turn_number / constants.MAX_TURNS + 400) * 2 / self.data.nbr_player
        self.data.max_turn_to_base = 0;
        self.data.nbr_turn_left = constants.MAX_TURNS - self.game.turn_number


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

#defini si c'est un enemy sur la position donnee
    def     is_enemy(pos) :
        if game_map[pos].is_occupied :
            if game_map[pos].is_occupied in self.me.get_ships() :
                return (0)
        return (1)


    def check_halite_around(self, ship):
        pad = 4
        total_ha = 0
        pos = ship.position
        for i in range(-pad, pad) :
            for j in range (-pad, pad) :
                total_ha += self.game.game_map[Position(pos.x + i, pos.y + j)].halite_amount
        return (total_ha)
