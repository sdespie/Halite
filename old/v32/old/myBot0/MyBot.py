#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction
from hlt.positionals import Position

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging


def load_constants(constants):
    """
    Load constants from JSON given by the game engine.
    """
    global SHIP_COST, DROPOFF_COST, MAX_HALITE, MAX_TURNS
    global EXTRACT_RATIO, MOVE_COST_RATIO
    global INSPIRATION_ENABLED, INSPIRATION_RADIUS, INSPIRATION_SHIP_COUNT
    global INSPIRED_EXTRACT_RATIO, INSPIRED_BONUS_MULTIPLIER, INSPIRED_MOVE_COST_RATIO


class   Zone :

    def __init__(self, x, y, halite, position) :
        self.x = x
        self.y = y
        self.halite = halite
        self.position = position
        

def     detect_closest_worth(game_map, ship, me, game, val):
    pos = ship.position
    max = 100
    for i in range(pos.x - val, pos.x + val):
        for j in range(pos.y - val, pos.y + val):
            if game.game_map[Position(i,j)].halite_amount > max and game.game_map[Position(i,j)].is_occupied == False:
                max = game.game_map[Position(i,j)].halite_amount
                max_pos = Position(i,j)
                
    if max > 100 :
     #   logging.info("Ship {} has target :{}.".format(ship.id, max_pos))
        return (max_pos)
    else :
        return (detect_closest_worth(game_map, ship, me, game, val + 1))


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
            
    return (Position(x + random.randint(-1, 1 ), y + random.randint(-1, 1)))
        


def    get_nbr_ships(list) :
    i = 0;
    for ships in list :
        i+=1
    return (i)


# fonction donnant la case avec le plus d'Halite en direct autour de la tortue avec mode 1, ou le moins avec mode 0
def    get_best_pos(pos, mode, ship, me, game_map) :
    if mode == 1 :
        if get_closest_drop_dist(ship, me, game_map) == 0:
            max = 0
        else :
            max = game_map[pos].halite_amount
        direction = pos
        for posi in pos.get_surrounding_cardinals() :
            if game_map[posi].halite_amount >= max and not game_map[posi].is_occupied :
                direction = posi
                max = game_map[posi].halite_amount
                
#        if get_closest_drop_dist(ship, me, game_map) :
#          if max < game_map[ship.position].halite_amount :
#                direction = ship.position
    else :
        min = game_map[pos].halite_amount
        direction = pos
        for posi in pos.get_surrounding_cardinals() :
            if game_map[posi].halite_amount < max and not game_map[posi].is_occupied :
                direction = posi
              #  game
                max = game_map[posi].halite_amount
                
    logging.info("Get Best pos return ={}.".format(direction))    
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
            
#defini si c'est un enemy sur la position donnee
def     is_enemy(ship, game_map, me) :
    if game_map[get_closest_drop_pos(ship, me, game_map)].is_occupied() :
        for ship in me.get_ships() :
            if ship.position == get_closest_drop_pos(ship, me, game_map) :
                return (1)
    return (0)

# Fonction to determine what to do depending on the situation
def     choose_action(ship, game_map, me, nbr_drop) :

 #   if get_closest_drop_dist(ship, me, game_map) < (game.turn_number - MAX_T) + 5  and get_closest_drop_dist(ship, me, game_map) != 1:
  #      return (5)
   # elif get_closest_drop_dist(ship, me, game_map) < (game.turn_number - MAX_T) + 5  and get_closest_drop_dist(ship, me, game_map) != 1:
    #    return (3)    
    if ship_status[ship.id] == "returning":
        #if get_closest_drop_dist(ship, me, game_map) == 1 : # and is_enemy(ship, game_map, me) :
         #   return (5)
        if get_closest_drop_dist(ship, me, game_map) == 0:
            ship_status[ship.id] = "exploring"
            return (6)
        else:
            return (1)

    elif ship.halite_amount >= 500 and game_map.calculate_distance(ship.position, get_closest_drop_pos(ship, me, game_map)) < 10:
            ship_status[ship.id] = "returning"
            return (1)
        
    elif ship.halite_amount >= 750 :
        ship_status[ship.id] = "returning"
        if nbr_drop < MAX_DROP and get_closest_drop_dist(ship, me, game_map) >= MAX_T / 20 and me.halite_amount >= constants.DROPOFF_COST and game.turn_number < 0.75 * MAX_T:
            return (2)
          
    if game_map[ship.position].halite_amount < 100 or ship.is_full and ship_status[ship.id] == "exploring":
        return (3)

    else:
        return (4)


# fait ce qui a ete deterniné dans la fonction choose_action
def     do_action(nbr, game_map, ship, me, game) :
    if nbr == 1 :
        move = game_map.naive_navigate(ship, get_closest_drop_pos(ship, me, game_map))
        command_queue.append(ship.move(move))
        
    elif nbr == 2 :
        command_queue.append(ship.make_dropoff())
        
    elif nbr == 3 : 
        move = game_map.naive_navigate(ship, detect_closest_worth(game_map, ship, me, game, 1))
        #move = game_map.naive_navigate(ship, get_best_pos(ship.position, 1, ship, me, game_map))
        #move = game_map.naive_navigate(ship, check_best_spot(game_map, ship, me, game))
        command_queue.append(ship.move(move))
        
    elif nbr == 4 :
        command_queue.append(ship.stay_still())
#    elif nbr == 5 :
 #       move = game_map.get_unsafe_moves(ship.position, get_closest_drop_pos(ship, me, game_map))
 #       command_queue.append(ship.move(move[0]))
    elif nbr == 6 :
        move = game_map.naive_navigate(ship, get_best_pos(ship.position, 1, ship, me, game_map))
        command_queue.append(ship.move(move))


 
""" <<<Game Begin>>> """


game = hlt.Game()
ship_status = {} 
game.ready("AsgardBot")
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))
nbr_drop = 0

MAX_T = constants.MAX_TURNS
if (MAX_T < 450) :
    MAX_DROP = 2
else :
    MAX_DROP = 3

""" <<<Game Loop>>> """




while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map
    nbr_ships = get_nbr_ships(me.get_ships())

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []
    construction = 0

    for ship in me.get_ships():

     #   logging.info("Ship {} has {} halite.".format(ship.id, ship.halite_amount))
 
        if ship.id not in ship_status:
            ship_status[ship.id] = "exploring"
        action = choose_action(ship, game_map, me, nbr_drop)
        if action == 2 :
            construction += 1
     #   logging.info("action is {}.".format(action))
        if action == 2 and construction > 1 :
            nbr_drop += 1
            do_action(3, game_map, ship, me, game)
        else :
            do_action(action, game_map, ship, me, game)

    #Spawn si pas dedropoff de prévu
    if construction == 0 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied :
        if game.turn_number <= MAX_T / 2.5 or nbr_ships < (MAX_T - game.turn_number) / 18 :
            command_queue.append(me.shipyard.spawn())


    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

#TEST CODE 