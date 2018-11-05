"""
------------------------------------ INIT IMPORT
"""

import hlt
from hlt import constants
from hlt.positionals import Direction
from hlt.perso_constants import *
from hlt.perso_map import *
from hlt.entity import *
from hlt.constants import *
from time import gmtime, strftime


import random
import logging


"""
----------------------------------------------------------------------Game Begin
"""

"""
-------- INIT STRUCT
"""

game = hlt.Game()
file = open("log/" + strftime("%Y-%m-%d %H:%M:%S", gmtime()), "a")

# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("MyAsgard2.0")
file.write("Successfully created bot! My Player ID is {}.\n".format(game.my_id))

data = Data_game()
data.ship_list = []
data.nbr_drop = 0
data.drop_duty = []
data.nbr_player = len(game.players.values())
data.max_turn_spawn = constants.MAX_TURNS * (0.5 +(game.game_map.height - 32) / 16 * 0.05)

#calc = Calc(game, data, game.me)
map = Map(game, data, game.me)#, calc)
file.write("Max turn spawn = {}.\n".format(data.max_turn_spawn))



"""
---------------------------------------------------------Game Loop
"""

while True:

    """
    ------------------------------------ RESET
    """

    game.update_frame()
    me = game.me
    game_map = game.game_map
    command_queue = []
    map.analyse_map()

    """
    ------------------------------------- MAJ LIST
    """
    


    """
    ------------------------------------ START
    """







    # Send your moves back to the game environment, ending this turn.


    """
    ------------------------------------- END
    """
    game.end_turn(command_queue)

file.close()
evolve = open("./evolve", "a")
evolve.write("Successfully created bot! My Player ID is {}.\n".format(game.my_id))
evole.close()
