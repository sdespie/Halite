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
from hlt.perso_algo import *
from hlt.entity import *
from hlt.constants import *
import random
import logging

from time import gmtime, strftime

'''
def     check_best_spot(game_map, ship, me, game)
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
'''

# fonction donnant la case avec le plus d'Halite en direct autour de la tortue avec mode 1, ou le moins avec mode 0




# Fonction to determine what to do depending on the situation
def     choose_action(ship, game_map, me, nbr_drop) :

 #   if get_closest_drop_dist(ship, me, game_map) < (game.turn_number - MAX_T) + 5  and get_closest_drop_dist(ship, me, game_map) != 1:
  #      return (5)
   # elif get_closest_drop_dist(ship, me, game_map) < (game.turn_number - MAX_T) + 5  and get_closest_drop_dist(ship, me, game_map) != 1:
    #    return (3)
    file.write("Ship {} is in action.\n".format(ship.id))

  #  if get_closest_drop_dist(ship, me, game_map) > nbr_turn_left * 1.2 + nbr_ships :
   #     if game_map[ship.position].halite_amount > ship.halite_amount * 10 :
   #         return ("stay")
   #     return(5)

    if game_map[ship.position].halite_amount > ship.halite_amount * 10:
        return ("stay")

    elif data.turtle_list[ship.id].status == "returning" :
        if calc.get_closest_drop_dist(ship) == 0 :
            return ("exploring")
        else :
            return ("returning")

    elif data.turtle_list[ship.id].status == "exploring" :
        if data.nbr_drop < MAX_DROP and ship.halite_amount >= 800 \
            and calc.get_closest_drop_dist(ship) >= MAX_T / 14 / data.nbr_player \
            and game.turn_number < 0.75 * MAX_T and overall.check_halite_around(ship) > 12000 \
            and data.nbr_ships >= 8 and (data.on_hold == 0 or ship.id in data.drop_duty):
            if me.halite_amount + ship.halite_amount + game_map[ship.position].halite_amount >= 4000 :
                data.on_hold = 0
                data.drop_duty = []
                file.write("------Ship {} created dropoff.\n".format(ship.id))
                return ("dropoff")
            else :
                data.drop_duty.append(ship.id)
                data.on_hold = 1
                file.write("-------Ship {} staying for dropoff.\n".format(ship.id))
                return ("stay")

        elif ship.halite_amount >= 950 :
            return ("returning")
        elif game_map[ship.position].halite_amount >= 100 :
            return ("stay")
        elif ship.halite_amount > 700 and calc.get_closest_drop_dist(ship) <= 7 :
            return ("returning")
        else :
            return ("exploring")
    else :
        return ("stay")



# fait ce qui a ete deterniné dans la fonction choose_action
def     do_action(nbr, game_map, ship, me, game, data) :
    file.write("Ship {} has action is {}.\n".format(ship.id, nbr))
    file.write("Ship {} has {} halite.\n".format(ship.id, ship.halite_amount))

    turtle.busy = 1

    if nbr == "returning" :
        action.returning(ship)

    elif nbr == "dropoff" :
        action.make_dropoff(ship)

    elif nbr == "exploring" :
        action.exploring(ship)

    elif nbr == "stay" :
        action.stay(ship)

    elif nbr == "suicide" :
        action.suicide(ship)

    elif nbr == "safety" :
        action.safety(ship)



def contains(list, filter):
    for turtle in list:
        if filter(turtle):
            return True
    return False





"""
-----------------------------------------------------------<<<Game Begin>>>
"""


game = hlt.Game()

file = open("log/" + strftime("%Y-%m-%d %H:%M:%S", gmtime()), "a")

MAX_T = constants.MAX_TURNS
data = Data_game()
overall = Overall(game, data, game.me)
calc = Calc(game, data, game.me)
action = Action(game, data, game.me, game_map, file, calc, overall)
data.nbr_drop = 0
data.on_hold = 0
#data.ship_status = {}
data.drop_duty = []
data.nbr_player = len(game.players.values())
ratio = (game.game_map.height - 32) / 16 * 0.05
data.max_turn_spawn = MAX_T * (0.5 + ratio)
file.write("data.max_turn = {}.\n".format(data.max_turn_spawn))


data.turtle_list = {}
if (MAX_T < 450) :
    MAX_DROP = 2
else :
    MAX_DROP = 3

game.ready("AsgardBot-v33")
file.write("Successfully created bot! My Player ID is {}.\n".format(game.my_id))



"""
---------------------------<<<Game Loop>>>
"""
while True:

    file.write("==== TURN {} TIME {:3.1f}% ====\n".format(game.turn_number, 100 * game.turn_number / constants.MAX_TURNS))
    game.update_frame()
    me = game.me
    game_map = game.game_map
    data.command_queue = []
    data.construction = 0
    ship_busy = []
    data.nbr_ships = len(me.get_ships())
    data.planned_pos = []
    data.planned_dest = []
    data.opp_pos = []
    data.nbr_turn_left = MAX_T - game.turn_number


    overall.analyse_map()


    for ship in me.get_ships() :
        if ship.id not in data.turtle_list.keys():
            turtle = Turtle(ship)
            data.turtle_list[ship.id] = turtle
            data.turtle_list[ship.id].status == "exploring"

    for ship in me.get_ships() :
        data.turtle_list[ship.id].position = ship.position
        data.turtle_list[ship.id].halite_amount = ship.halite_amount


    '''    ship = Turtle(ship)
        if calc.get_closest_drop_dist(ship) > data.max_turn_to_base :
            data.max_turn_to_base = calc.get_closest_drop_dist(ship)
    '''
    '''
    if  data.nbr_turn_left * 1.1 + data.nbr_ships < data.max_turn_to_base:
        for ship in me.get_ships():
            ship_busy.append(ship)
            if  ship.halite_amount < game_map[ship.position].halite_amount * 10 :
                do_action("stay", ship)
            elif calc.get_closest_drop_dist(ship) == 1 :
                do_action(5, game_map, ship, me, game)
            else :
                do_action(1, game_map, ship, me, game)
    '''
    '''
    Mise a jour de la liste Turtle tour apres autour, garde les anciennes tortues, retire les mortes


    for ship in me.get_ships():
        file.write("Ship.id =  {}.\n".format(ship.id))
        ship = Turtle(ship)
        if contains(turtle_list, lambda turtle: turtle.id == ship.id):
            file.write("Append.\n")
            turtle_list.append(ship)

    for turtle in turtle_list:
        if not contains(me.get_ships(), lambda ship: ship.id == turtle.id):
            file.write("Removed.\n")
            turtle_list.remove(turtle.id)
    '''

    for turtle in data.turtle_list.values():
#        if turtle.id not in data.ship_status:
#            data.ship_status[turtle.id] = "exploring"
        if turtle.busy == 0:
            choice = choose_action(turtle, game_map, me, data.nbr_drop)
            if choice == "stay" :
                do_action(choice, game_map, turtle, me, game, data)


    for turtle in data.turtle_list.values():
        if turtle.busy == 0 :
            choice = choose_action(turtle, game_map, me, data.nbr_drop)
            if choice == "dropoff" :
                data.construction += 1
            if choice == "dropoff" and data.construction > 1 :
                data.nbr_drop += 1
                choice = "exploring"
            if choice == "safety" or choice == "dropoff" :
                do_action(choice, game_map, turtle, me, game, data)

    for turtle in data.turtle_list.values():
        if turtle.busy == 0:
            choice = choose_action(turtle, game_map, me, data.nbr_drop)
            file.write("Ship {} has action is {}.\n".format(turtle.id, choice))
            if choice != "dropoff" and choice != "stay" and choice != "safety" or (choice == "dropoff" and data.construction > 1) :
                if choice == "dropoff" :
                    do_action("exploring", game_map, turtle, me, game, data)
                else :
                    do_action(choice, game_map, turtle, me, game, data)


    if data.construction == 0 and me.halite_amount >= constants.SHIP_COST:
        file.write("J'aimerais peut etre spawn!.\n".format())
        if  me.shipyard.position not in data.planned_pos and data.construction == 0:
            file.write("J'aimerais spawn!.\n".format())
            if game.turn_number <= data.max_turn_spawn and data.on_hold == 0 :
                data.command_queue.append(me.shipyard.spawn())
                file.write("Je Sapwn!.\n".format())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(data.command_queue)


file.close()
