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
from hlt.entity import *
from hlt.constants import *
import random
import logging

from time import gmtime, strftime



def     detect_closest_worth(game_map, ship, me, game, val, max):
    pos = ship.position
    new_max = max
    for i in range(pos.x - val, pos.x + val):
        for j in range(pos.y - val, pos.y + val):
            if game.game_map[Position(i,j)].halite_amount > new_max and game.game_map[Position(i,j)].is_occupied == False:
                new_max = game.game_map[Position(i,j)].halite_amount
                max_pos = Position(i,j)

    if new_max > max :
       #file.write("Ship {} has target :{}.\n".format(ship.id, max_pos))
        return (max_pos)
    elif val >= game_map.height / 2:
        return (detect_closest_worth(game_map, ship, me, game, 1, max / 2))
    else :
        return (detect_closest_worth(game_map, ship, me, game, val + 1, max))

def     check_best_spot(game_map, ship, me, game) :
    list = []

    x = 0
    y = 0
    i = 0


    while (x < 56):
        y = 0
        while (y < 56):
            halite = 0
            zone = Zone(x, y, halite, Position(x, y))
            while (i < 8):
                j = 0
                while (j < 8):
                    zone.halite += game_map[Position(x + i, y + j)].halite_amount
                    j += 1
                i += 1
            list.append(zone)
            y += 8
        x += 8
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



def    get_nbr_ships(list) :
    i = 0;
    for ships in list :
        i += 1
    return (i)




# fonction donnant la case avec le plus d'Halite en direct autour de la tortue avec mode 1, ou le moins avec mode 0
def    get_best_pos(pos, mode, ship, me, game_map) :
    if mode == 1 :
        max = 0
        direction = pos
        for posi in pos.get_surrounding_cardinals() :
            if game_map[posi].halite_amount >= max and posi not in data.planned_pos :
                direction = posi
                max = game_map[posi].halite_amount


    else :
        min = game_map[pos].halite_amount
        direction = pos
        for posi in pos.get_surrounding_cardinals() :
            if game_map[posi].halite_amount < max and not game_map[posi].is_occupied :
                direction = posi
                max = game_map[posi].halite_amount

    #file.write("Get Best pos return ={}.\n".format(direction))
    return (direction)

# Donne la distance la plus courte etre le ship actuel et le dropoff ou shipyard le plus proche
def     get_closest_drop_dist(ship, me, game_map) :
    min = game_map.calculate_distance(ship.position, me.shipyard.position)
    for dropoff in me.get_dropoffs() :
        if min > game_map.calculate_distance(ship.position, dropoff.position) :
            min = game_map.calculate_distance(ship.position, dropoff.position)
    return (min)

# donne la position du dropoff ou shipyard le plus proche d'un ship
def     get_closest_drop_pos(ship, me, game_map) :
    min = game_map.calculate_distance(ship.position, me.shipyard.position)
    pos = me.shipyard.position
    for dropoff in me.get_dropoffs() :
        if min > game_map.calculate_distance(ship.position, dropoff.position) :
            min = game_map.calculate_distance(ship.position, dropoff.position)
            pos = dropoff.position
    return (pos)



#defini la prochaine position que prendre le ship
def     get_next_pos(ship, objectif, game_map, me) :
    move = game_map.get_unsafe_moves(ship.position, objectif)
    for direction in move :
        direct = get_correct_dir(ship, direction)
        if direct not in data.planned_pos and not overall.is_enemy(direct) :
            return (direct)
    move = get_best_pos(ship.position, 1, ship, me, game_map)
    return (move)



# Fonction to determine what to do depending on the situation
def     choose_action(ship, game_map, me, nbr_drop) :

 #   if get_closest_drop_dist(ship, me, game_map) < (game.turn_number - MAX_T) + 5  and get_closest_drop_dist(ship, me, game_map) != 1:
  #      return (5)
   # elif get_closest_drop_dist(ship, me, game_map) < (game.turn_number - MAX_T) + 5  and get_closest_drop_dist(ship, me, game_map) != 1:
    #    return (3)
    #file.write("Ship {} is in action.\n".format(ship.id))

  #  if get_closest_drop_dist(ship, me, game_map) > nbr_turn_left * 1.2 + nbr_ships :
   #     if game_map[ship.position].halite_amount > ship.halite_amount * 10 :
   #         return ("stay")
   #     return(5)

    if game_map[ship.position].halite_amount > ship.halite_amount * 10 and ship.position not in opp_pos:
        return ("stay")

    elif ship_status[ship.id] == "returning" :
        if get_closest_drop_dist(ship, me, game_map) == 0 :
            return (3)
        else :
            return (1)

    elif ship_status[ship.id] == "exploring" :
        if data.nbr_drop < 2 and ship.halite_amount >= 800 \
            and get_closest_drop_dist(ship, me, game_map) >= MAX_T / 17 / data.nbr_player \
            and game.turn_number < 0.75 * MAX_T and overall.check_halite_around(ship) > 12000 \
            and data.nbr_ships >= 8 and (data.on_hold == 0 or ship.id in data.drop_duty):
            if me.halite_amount + ship.halite_amount >= 4000 :
                data.on_hold = 0
                data.drop_duty = []
               #file.write("------Ship {} created dropoff.\n".format(ship.id))
                return (2)
            else :
                data.drop_duty.append(ship.id)
                data.on_hold = 1
               #file.write("-------Ship {} staying for dropoff.\n".format(ship.id))
                return ("stay")

        elif ship.halite_amount >= 900 :
            return (1)
        elif ship.halite_amount > 700 and get_closest_drop_dist(ship, me, game_map) <= 7 :
            return (1)
        elif game_map[ship.position].halite_amount >= 100 :
            return ("stay")
        else :
            return (3)

    else :
        return ("stay")




# fait ce qui a ete deterniné dans la fonction choose_action
def     do_action(nbr, game_map, ship, me, game, data) :
   #file.write("Ship {} has action is {}.\n".format(ship.id, nbr))
    #file.write("Ship {} has {} halite.\n".format(ship.id, ship.halite_amount))

    turtle.busy = 1

    if nbr == 1 :
        ship_status[ship.id] = "returning"
        move = game_map.get_unsafe_moves(ship.position, get_closest_drop_pos(ship, me, game_map))
        for direction in move :
            direct = overall.get_correct_dir(ship.position, direction)
            if direct not in data.planned_pos and direct not in data.planned_dest and direct not in opp_pos:
                #file.write("Ship {} is action 1, going to {}.\n".format(ship.id, action, direct))
                data.planned_dest.append(direct)
                data.planned_pos.append(direct)
                command_queue.append(ship.move(direction))
                return
        do_action(6, game_map, ship, me, game, data)

    elif nbr == 2 :
       #file.write("---------Ship {} is action {}, doing a dropoff at {}.\n".format(ship.id, action, ship.position))
        data.planned_dest.append(ship.position)
        data.planned_pos.append(ship.position)
        command_queue.append(ship.make_dropoff())

    elif nbr == 3 :
        ship_status[ship.id] = "exploring"
        move = game_map.get_unsafe_moves(ship.position, detect_closest_worth(game_map, ship, me, game, 1, data.max_radar))
        for direction in move :
            direct = overall.get_correct_dir(ship.position, direction)
            if direct not in data.planned_pos and direct not in data.planned_dest and direct not in opp_pos:
               #file.write("Ship {} is action {}, going to {}, with {}.\n".format(ship.id, action, direct, game_map[direct].halite_amount))
                data.planned_dest.append(direct)
                data.planned_pos.append(direct)
                command_queue.append(ship.move(direction))
                return
        do_action(6, game_map, ship, me, game, data)

    elif nbr == "stay" :
        data.planned_dest.append(ship.position)
        data.planned_pos.append(ship.position)
       #file.write("Ship {} is action {}, staying at {}.\n".format(ship.id, action, ship.position))
        command_queue.append(ship.stay_still())

    elif nbr == 5 :
        move = game_map.get_unsafe_moves(ship.position, get_closest_drop_pos(ship, me, game_map))
       #file.write("Ship {} is action {}, suicidee.\n".format(ship.id, action))
        command_queue.append(ship.move(move[0]))

    elif nbr == 6 :
        move = game_map.get_unsafe_moves(ship.position, get_best_pos(ship.position, 1, ship, me, game_map))
        for direction in move :
            direct = overall.get_correct_dir(ship.position, direction)
            if direct not in data.planned_pos and direct not in data.planned_dest and direct not in opp_pos:
               #file.write("Ship {} is action {}, going to 6 to {}.\n".format(ship.id, action, direct))
                data.planned_pos.append(direct)
                data.planned_dest.append(direct)
                command_queue.append(ship.move(direction))
                return
        #do_action(4, game_map, ship, me, game)

def contains(list, filter):
    for turtle in list:
        if filter(turtle):
            return True
    return False

""" <<<Game Begin>>> """


game = hlt.Game()
ship_status = {}
#file = open("log/" + strftime("%Y-%m-%d %H:%M:%S", gmtime()), "a")


game.ready("AsgardBot")
#file.write("Successfully created bot! My Player ID is {}.\n".format(game.my_id))





MAX_T = constants.MAX_TURNS
if (MAX_T < 450) :
    MAX_DROP = 2
else :
    MAX_DROP = 3

""" <<<Game Loop>>> """
turtle_list = []
data = Data_game()
overall = Overall(game, data, game.me)
data.nbr_drop = 0
data.on_hold = 0
data.drop_duty = []

while True:

   #file.write("==== TURN {} TIME {:3.1f}% ====\n".format(game.turn_number, 100 * game.turn_number / constants.MAX_TURNS))
    game.update_frame()
    me = game.me
    game_map = game.game_map
    command_queue = []
    data.construction = 0
    ship_busy = []
    data.nbr_ships = get_nbr_ships(me.get_ships())
    data.planned_pos = []
    data.planned_dest = []
    data.opp_pos = []
    data.turtle_list = []


    if game.turn_number == 1:
        data.nbr_player = 0
        overall.get_players_nbr()

    opp_pos = []
    overall.analyse_map()

    for ship in me.get_ships() :
        if get_closest_drop_dist(ship, me, game_map) > data.max_turn_to_base :
            max_turn_to_base = get_closest_drop_dist(ship, me, game_map)


    '''  if  nbr_turn_left < max_turn_to_base + 2 :
        for ship in me.get_ships():
            ship_busy.append(ship)
            if  ship.halite_amount < game_map[ship.position].halite_amount * 10 :
                do_action("stay", game_map, ship, me, game)
            elif get_closest_drop_dist(ship, me, game_map) == 1 :
                do_action(5, game_map, ship, me, game)
            else :
                do_action(1, game_map, ship, me, game)'''

    '''
    Mise a jour de la liste Turtle tour apres autour, garde les anciennes tortues, retire les mortes


    for ship in me.get_ships():
       #file.write("Ship.id =  {}.\n".format(ship.id))
        ship = Turtle(ship)
        if contains(turtle_list, lambda turtle: turtle.id == ship.id):
           #file.write("Append.\n")
            turtle_list.append(ship)

    for turtle in turtle_list:
        if not contains(me.get_ships(), lambda ship: ship.id == turtle.id):
           #file.write("Removed.\n")
            turtle_list.remove(turtle.id)
    '''

    for ship in me.get_ships():
        ship = Turtle(ship)
        turtle_list.append(ship)


    for turtle in turtle_list:
        if turtle.id not in ship_status:
            ship_status[turtle.id] = "exploring"
        if turtle.busy == 0:
            action = choose_action(turtle, game_map, me, data.nbr_drop)
            if action == "stay" :
                do_action(action, game_map, turtle, me, game, data)


    for turtle in turtle_list:
        if turtle.busy == 0 :
            action = choose_action(turtle, game_map, me, data.nbr_drop)
            if action == 2 :
                data.construction += 1
            if action == 2 and data.construction > 1 :
                data.nbr_drop += 1
                action = 3
            if action == 6 or action == 2 :
                do_action(action, game_map, turtle, me, game, data)

    for turtle in turtle_list:
        if turtle.busy == 0:
            action = choose_action(turtle, game_map, me, data.nbr_drop)
           #file.write("Ship {} has action is {}.\n".format(ship.id, action))
            if action != 2 and action != "stay" and action != 6 or (action == 2 and data.construction > 1) :
                if action == 2 :
                    do_action(3, game_map, turtle, me, game, data)
                else :
                    do_action(action, game_map, turtle, me, game, data)


    if data.construction == 0 and me.halite_amount >= constants.SHIP_COST and data.on_hold == 0:
        if  me.shipyard.position not in data.planned_pos :
            if game.turn_number <= MAX_T / 3 * 2 / min(data.nbr_player, 3)  :#or nbr_ships < (MAX_T - game.turn_number) / 10 :
                command_queue.append(me.shipyard.spawn())

                #file.write("Je Sapwn!.\n".format())


    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)


file.close()
