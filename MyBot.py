#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import *
from hlt.positionals import *
from hlt.perso_ft import *
from hlt.perso_ship import *
from hlt.perso_utils import *
from hlt.entity import *
from hlt.constants import *
from hlt.perso_const import *
import random
import logging

from time import gmtime, strftime


def     check_best_spot(game_map, ship, me, game) :
    list = []

    x = 0
    y = 0
    i = 0

    while (x < game_map.height):
        y = 0
        while (y < game_map.height):
            halite = 0
            zone = Zone(x, y, halite, Position(x, y))
            while (i < 8):
                j = 0
                while (j < 8):
                    zone.halite += game_map[Position(x + i, y + j)].halite_amount
                    j += 1
                i += 1
            list.append(zone)
            y += 1
        x += 1
    max = 0

    for zone in list :
        if game_map.calculate_distance(zone.position, ship.position) == 0 :
            dist = 1
        else :
            dist = game_map.calculate_distance(zone.position, ship.position)
        if zone.halite / dist > max :
            if game_map.calculate_distance(zone.position, ship.position) == 0 :
                dist = 1
            else :
                dist = game_map.calculate_distance(zone.position, ship.position)
            max = zone.halite / dist
            x = zone.x + 4
            y = zone.y + 4

    return (Position(x + random.randint(-1, 1), y + random.randint(-1, 1)))


# fonction donnant la case avec le plus d'Halite en direct autour de la tortue avec mode 1, ou le moins avec mode 0
def    get_best_pos(pos, mode, ship, me, game_map) :
    if mode == 1 :
        max = 0
        direction = pos
        for posi in pos.get_surrounding_cardinals() :
            if game_map[posi].halite_amount >= max and posi not in data.planned_pos and posi not in data.opp_pos:
                direction = posi
                max = game_map[posi].halite_amount

    else :
        min = game_map[pos].halite_amount
        direction = pos
        for posi in pos.get_surrounding_cardinals() :
            if game_map[posi].halite_amount < max and not game_map[posi].is_occupied and posi not in data.opp_pos:
                direction = posi
                max = game_map[posi].halite_amount

    return (direction)



"""
-------------------------------------------------------- ACTION
"""



"""
-----------------------------------------CHOOSE_ACTIONS
"""

# Fonction to determine what to do depending on the situation
def     choose_action(ship, game_map, me, nbr_drop) :

    if calc.get_closest_drop_dist(ship.position) * 1.1 > (MAX_T - game.turn_number) :
        data.suicide = 1
    min_mine = min(50, 0.6 * data.total_halite / (game_map.height * game_map.height))

    #utils.print_log("Min MINE = {}".format(min_mine), file)
    #utils.print_log("Ship ID = {}, Closest drop dist = {}, Other side = {}".format(ship.id, calc.get_closest_drop_dist(ship.position), (MAX_T - game.turn_number) * 1.1 + data.nbr_ships), file)
    if game_map[ship.position].halite_amount > ship.halite_amount * 10 :
        return ("stay")

    elif data.suicide == 1:
        if calc.get_closest_drop_dist(ship.position) != 1 :
            return ("returning")
        else :
            return ("suicide")

    elif game_map[ship.position].halite_amount * 0.25 + ship.halite_amount >= RETURN_HALITE \
        and ship.halite_amount < RETURN_HALITE \
        and ship_status[ship.id] != "returning" and \
            ship.position not in data.planned_pos :
        return ("stay")

    elif ship_status[ship.id] == "returning" :
        if calc.get_closest_drop_dist(ship.position) == 0 :
            return ("exploring")
        else :
            return ("returning")

    elif ship_status[ship.id] == "exploring" :
        if ship.halite_amount >= 800 \
            and data.construction == 0 \
            and calc.get_closest_drop_dist(ship.position) >= 10 + (game.game_map.height - 32) / DROP_DIST_RATIO * (2 / data.nbr_player) \
            and game.turn_number < DROP_MAX_TURN_RATIO * MAX_T and overall.check_halite_around(ship) > 17000 \
            and data.nbr_ships >= DROP_MIN_SHIP and (data.on_hold == 0 or ship.id in data.drop_duty): # and data.nbr_drop < MAX_DROP and:
            if me.halite_amount + ship.halite_amount + game_map[ship.position].halite_amount >= 4000 :
                data.on_hold = 0
                data.drop_duty = []
                data.construction += 1
                data.nbr_drop += 1
                utils.print_log("------Ship {} created dropoff.".format(ship.id), file)
                return ("dropoff")
            else :
                data.drop_duty.append(ship.id)
                data.on_hold = 1
                utils.print_log("-------Ship {} staying for dropoff.".format(ship.id), file)
                return ("stay")

        elif ship.halite_amount >= RETURN_HALITE :
            return ("returning")
        elif game_map[ship.position].halite_amount >= data.min_mine and \
            ship.position not in data.planned_pos :
            return ("stay")
        elif ship.halite_amount > 700 and calc.get_closest_drop_dist(ship.position) <= 7 :
            return ("returning")
        else :
            return ("exploring")

    else :
        return ("stay")


"""
-------------------------------------------- ACTIONS
"""

'''RETURNING'''

def returning(game_map, ship, me, game, data, calc):
    ship_status[ship.id] = "returning"
    move = game_map.get_unsafe_moves(ship.position, calc.get_closest_drop_pos(ship))
    if len(move) == 2 :
        min_halite = 1200
        for direction in move :
            direct = overall.get_correct_dir(ship.position, direction)
            if direct not in data.planned_pos and direct not in data.planned_dest and direct not in data.opp_pos :
                if min_halite > game_map[direct].halite_amount :
                    min_halite = game_map[direct].halite_amount
                    ret = direct
                    retour = direction
        if min_halite < 1200 :
            utils.print_log("Ship {} is action returning, going to {}.".format(ship.id, ret), file)
            data.planned_dest.append(ret)
            data.planned_pos.append(ret)
            command_queue.append(ship.move(retour))
            return
    elif len(move) == 1 :
            for direction in move :
                direct = overall.get_correct_dir(ship.position, direction)
                if direct not in data.planned_pos and direct not in data.planned_dest and direct not in data.opp_pos:
                    utils.print_log("Ship {} is action returning, going to {}.".format(ship.id, direct), file)
                    data.planned_dest.append(direct)
                    data.planned_pos.append(direct)
                    command_queue.append(ship.move(direction))
                    return
    if ship.position in data.planned_pos or ship.position in data.opp_pos :
        do_action("security", game_map, ship, me, game, data, calc)
    else :
        do_action("stay", game_map, ship, me, game, data, calc)


'''DROPOFF'''

def dropoff(game_map, ship, me, game, data, calc):
    utils.print_log("---------Ship {} is action dropoff, doing a dropoff at {}.".format(ship.id, ship.position), file)
    command_queue.append(ship.make_dropoff())

'''EXPLORING'''

def exploring(game_map, ship, me, game, data, calc):
    ship_status[ship.id] = "exploring"
    move = game_map.get_unsafe_moves(ship.position, calc.detect_closest_worth(ship, 1, data.max_radar))
    if len(move) == 2 :
        max_halite = 0
        for direction in move :
            #utils.print_log("Ship {} pre correct dir = {}".format(ship.id, direction), file)
            direct = overall.get_correct_dir(ship.position, direction)
            #utils.print_log("Ship {} post correct dir = {}".format(ship.id, direct), file)
            if direct not in data.planned_pos and direct not in data.planned_dest and direct not in data.opp_pos:
                if max_halite < game_map[direct].halite_amount :
                    max_halite = game_map[direct].halite_amount
                    ret = direct
                    retour = direction
        if max_halite > 0 :
            utils.print_log("Ship {} is action exploring, going to {}, with {}.".format(ship.id, direct, game_map[direct].halite_amount), file)
            data.planned_dest.append(ret)
            data.planned_pos.append(ret)
            command_queue.append(ship.move(retour))
            return
    elif len(move) == 1 :
        for direction in move :
            direct = overall.get_correct_dir(ship.position, direction)
            if direct not in data.planned_pos and direct not in data.planned_dest and direct not in data.opp_pos:
                utils.print_log("Ship {} is action returning, going to {}.".format(ship.id, direct), file)
                data.planned_dest.append(direct)
                data.planned_pos.append(direct)
                command_queue.append(ship.move(direction))
                return

    do_action("security", game_map, ship, me, game, data, calc)

'''STAY'''

def stay(game_map, ship, me, game, data, calc):
        data.planned_dest.append(ship.position)
        data.planned_pos.append(ship.position)
        utils.print_log("Ship {} is action stay, staying at {}.".format(ship.id, ship.position), file)
        command_queue.append(ship.stay_still())

'''SUICIDE'''

def suicide(game_map, ship, me, game, data, calc):
    move = game_map.get_unsafe_moves(ship.position, calc.get_closest_drop_pos(ship))
    utils.print_log("Ship {} is action suicide.".format(ship.id), file)
    command_queue.append(ship.move(move[random.randint(0, len(move) - 1)]))

'''SECURITY'''

def security(game_map, ship, me, game, data, calc) :
    '''    if ship_status[ship.id] == "returning" :
            do_action("stay", game_map, ship, me, game, data, calc)
            return
        else :'''
    move = game_map.get_unsafe_moves(ship.position, get_best_pos(ship.position, 1, ship, me, game_map))
    for direction in move :
        direct = overall.get_correct_dir(ship.position, direction)
        if direct not in data.planned_pos and direct not in data.planned_dest and direct not in data.opp_pos:
            utils.print_log("Ship {} is action security, going to security to {}.".format(ship.id, direct), file)
            data.planned_pos.append(direct)
            data.planned_dest.append(direct)
            command_queue.append(ship.move(direction))
            return
    do_action("stay", game_map, ship, me, game, data, calc)


"""
----------------------------------------- DO_ACTIONS
"""
# fait ce qui a ete deterniné dans la fonction choose_action
def     do_action(nbr, game_map, ship, me, game, data, calc) :
    utils.print_log("Ship {} is in DO_ACTION has action is {} and has {} Halite.".format(ship.id, nbr, ship.halite_amount), file)

    ship.busy = 1

    if nbr == "returning" :
        returning(game_map, ship, me, game, data, calc)

    elif nbr == "dropoff" :
        dropoff(game_map, ship, me, game, data, calc)

    elif nbr == "exploring" :
        exploring(game_map, ship, me, game, data, calc)

    elif nbr == "stay" :
        stay(game_map, ship, me, game, data, calc)

    elif nbr == "suicide" :
        suicide(game_map, ship, me, game, data, calc)


    elif nbr == "security" :
        security(game_map, ship, me, game, data, calc)

    else:
        utils.print_log("Je fais rien en fait, wtf", file)



def check_nbr_pos (turtle):
    i = 0

    if game.game_map[turtle.position].halite_amount > turtle.halite_amount * 10:
        turtle.nbr_choice = 0
        return
    if game.game_map[turtle.position].halite_amount >= data.min_mine and \
        ship_status[turtle.id] == "exploring" and \
        turtle.halite_amount <= RETURN_HALITE:
        turtle.nbr_choice = 0
        return
    if overall.get_correct_dir(turtle.position, (0, 0)) not in data.opp_pos and \
    overall.get_correct_dir(turtle.position, (0, 0)) not in data.planned_pos:
        i += 1
    if overall.get_correct_dir(turtle.position, (-1, 0)) not in data.opp_pos and \
    overall.get_correct_dir(turtle.position, (-1, 0)) not in data.planned_pos :
        i += 1
    if overall.get_correct_dir(turtle.position, (1, 0)) not in data.opp_pos and \
    overall.get_correct_dir(turtle.position, (1, 0)) not in data.planned_pos :
        i += 1
    if overall.get_correct_dir(turtle.position, (0, -1)) not in data.opp_pos and \
    overall.get_correct_dir(turtle.position, (0, -1)) not in data.planned_pos :
        i += 1
    if overall.get_correct_dir(turtle.position, (0, 1)) not in data.opp_pos and \
    overall.get_correct_dir(turtle.position, (0, 1)) not in data.planned_pos :
        i += 1
    turtle.nbr_choice = i

def update_pos() :
    for turtle in turtle_list :
        check_nbr_pos(turtle)

"""
----------------------------------------------------------------------------------<<<Game Begin>>>
"""


game = hlt.Game()
ship_status = {}
utils = Utils()
file = open("log/" + strftime("%Y-%m-%d %H:%M:%S", gmtime()), "a")
me = game.me
#file = 0

game.ready("AsgardBot")
utils.print_log("Successfully created bot! My Player ID is {}.".format(game.my_id), file)


MAX_T = constants.MAX_TURNS
if (MAX_T < 450) :
    MAX_DROP = 2
else :
    MAX_DROP = 3

turtle_list = []
data = Data_game()
calc = Calc(game, data, game.me)
overall = Overall(game, data, game.me, calc)
data.nbr_drop = 0
data.on_hold = 0
data.drop_duty = []
data.nbr_player = len(game.players.values())

ratio = ((game.game_map.height - 32) / MAX_TURN_RATIO * 0.05)
max_turn = MAX_T * (0.5 - (data.nbr_player - 2) * 0.05 + ratio)
utils.print_log("Max Turn = {}, Nbr Turn : {}, nbr_player = {}.".format(max_turn, MAX_T, data.nbr_player), file)

"""
-----------------------------------------------------------------<<<Game Loop>>>
"""
while True:

    """
    --------------- RESET
    """


    utils.print_log("\n==== TURN {} TIME {:3.1f}% ====\n".format(game.turn_number, 100 * game.turn_number / constants.MAX_TURNS), file)
    game.update_frame()
    me = game.me
    game_map = game.game_map
    command_queue = []
    data.construction = 0
    ship_busy = []
    data.nbr_ships = len(me.get_ships())
    data.planned_pos = []
    data.planned_dest = []
    data.opp_pos = []
    data.turtle_list = []
    data.total_halite = 0

    """
    -------------- STARTING CALC
    """

    overall.analyse_map()
    for i in range(0, game_map.height - 1) :
        for j in range (0, game_map.height - 1) :
            data.total_halite += game.game_map[Position(i, j)].halite_amount

    data.average_halite = data.total_halite / (game_map.height * game_map.height)
    data.min_mine = min([50, MIN_MINE_RATIO * data.average_halite])
    utils.print_log("Min_mine = {}".format(data.min_mine), file)

    for ship in me.get_ships():
        ship = Turtle(ship)
        turtle_list.append(ship)

    for turtle in turtle_list :
        if turtle.id not in ship_status:
            ship_status[turtle.id] = "exploring"



    """
    -------------- CALC
    """

    while len(turtle_list) != 0 :
        update_pos()
        min_pos = 6
        for turtle in turtle_list :
            if turtle.nbr_choice < min_pos :
                min_pos = turtle.nbr_choice
                if min_pos == 0 :
                    break
        for turtle in turtle_list :
            if turtle.nbr_choice <= min_pos :
                #utils.print_log("J'ai {} choix et {} Halite".format(turtle.nbr_choice, turtle.halite_amount), file)
                action = choose_action (turtle, game.game_map, me, data.nbr_drop)
                do_action(action, game.game_map, turtle, me, game, data, calc)
                turtle_list.remove(turtle)
                if min_pos > 0 :
                    break


    """
    -------------- SPAWN?
    """
    #utils.print_log("Je Sapwn ? data.construction = {}, halite_amount: {}".format(data.construction, me.halite_amount), file)
    if data.construction == 0 and me.halite_amount >= constants.SHIP_COST and data.on_hold == 0:
        if  me.shipyard.position not in data.planned_pos :
            if game.turn_number <= max_turn :
                command_queue.append(me.shipyard.spawn())
                utils.print_log("Je Sapwn! data.construction = {}, halite_amount: {}".format(data.construction, me.halite_amount), file)

    """
    -------------- SEND COMMAND
    """
    game.end_turn(command_queue)


"""
-------------- CLOSE FILES
"""

file.close()

#stats = open("stats", "a")
#utils.print_log("Joueur : {} ".format(game.my_id), stats)

#stats.close()
