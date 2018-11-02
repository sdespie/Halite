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

class Action :
    def __init__(self, game, data, me, game_map, file, calc, overall):
        self.game = game
        self.data = data
        self.me = me
        self.game_map = game_map
        self.file = file
        self.calc = calc
        self.overall = overall


    def exploring(self, ship):
        self.data.turtle_list[ship.id].status = "exploring"
        move = self.game.game_map.get_unsafe_moves(ship.position, self.calc.detect_closest_worth(ship, 1, self.data.max_radar))
        for direction in move :
            direct = self.overall.get_correct_dir(ship.position, direction)
            if direct not in self.data.planned_pos and direct not in self.data.planned_dest and direct not in self.data.opp_pos:
                self.file.write("Ship {} is exploring, going to {}, with {}.\n".format(ship.id, direct, self.game.game_map[direct].halite_amount))
                self.data.planned_dest.append(direct)
                self.data.planned_pos.append(direct)
                self.data.command_queue.append(ship.move(direction))
                return
        self.safety(ship)


    def returning(self, ship):
        self.data.turtle_list[ship.id].status = "returning"
        move = self.game.game_map.get_unsafe_moves(ship.position, self.calc.get_closest_drop_pos(ship))
        for direction in move :
            direct = self.overall.get_correct_dir(ship.position, direction)
            if direct not in self.data.planned_pos and direct not in self.data.planned_dest and direct not in self.data.opp_pos:
                self.file.write("Ship {} is action returning, going to {}.\n".format(ship.id, direct))
                self.data.planned_dest.append(direct)
                self.data.planned_pos.append(direct)
                self.data.command_queue.append(ship.move(direction))
                return
        self.safety(ship)




    def make_dropoff(self, ship):
        self.file.write("---------Ship {} = Make Dropoff, doing a dropoff at {}.\n".format(ship.id, ship.position))
        self.data.command_queue.append(ship.make_dropoff())



    def safety(self, ship):
        move = self.game.game_map.get_unsafe_moves(ship.position, self.calc.get_best_pos(ship.position, ship))
        for direction in move :
            direct = self.overall.get_correct_dir(ship.position, direction)
            if direct not in  self.data.planned_pos and direct not in self.data.planned_dest and direct not in  self.data.opp_pos:
                self.file.write("Ship {} = Safety, going to 6 to {}.\n".format(ship.id, direct))
                self.data.planned_pos.append(direct)
                self.data.planned_dest.append(direct)
                self.data.command_queue.append(ship.move(direction))
                return
        self.file.write("Ship {} = voulait rien faire, donc stay\n".format(ship.id))
        self.stay(ship)

    def stay (self, ship):
        self.data.planned_dest.append(ship.position)
        self.data.planned_pos.append(ship.position)
        self.file.write("Ship {} = Stay, staying at {}.\n".format(ship.id, ship.position))
        self.data.command_queue.append(ship.stay_still())



    def suicide(self, ship):
        move = self.game.game_map.get_unsafe_moves(ship.position, self.calc.get_closest_drop_pos(ship))
        self.file.write("Ship {} = Suicide, to {}.\n".format(ship.id, self.calc.get_closest_drop_pos(ship)))
        self.data.command_queue.append(ship.move(move[0]))
