# Halite III
This project is a Python AI to take part in the Halite III contest. This was my first contact with Python and I wanted to take that tournament as an opportinity to learn that language.
Please also notice that the way it's written is meant to be efficient for me to work on during that tournament period, not for you to read! :-D

# Thanks!

Thanks to Two Sigma for the awesome competition. I was happy to join this third edition! Can't wait for the next one.

# Bot Summary

Heres a quick summary of how my bot works:

* Gather map data per turn:  Generate the data structure to be used throughout the bot.
* Ennemies: Creating safe zones depending on enemies' position. Marking enemy ships with high halite for potential attacks.
* Retreat:  Determine whether its time to retreat (end game). 
* Priority queue: Determine a priority order of the ships, based on the amount of moves they can do.
* Build: Determine ships that will be building a dock.
* Attack: Move ships and support ships toward a certain target.
* Explore Target: Determine each ships target cell.
* Deposit: Move ships returning/depositing.
* Harvest: Move ships harvesting at its current position.
* Explore: Move remaining ships to its target locations.
* Processing the queue: Processing all ships with le lowest move possibility, then update the queue, repeat.
* Spawn: Determine if we are spawning a ship.

## Initialization

Each bot has 30 seconds to precompute or analyze the map.  I didnt really get to utilize this time that much. This time is mostly used for initializing structures and lists. 

## Gather Data

Here I generate a lot of parameters/variables that are used throughout the bot.  But mostly, this is where I generate a lot of numpy arrays, such as:
* Ship locations
* Dock locations
* Ship cargo
* Halite amount
* Potential enemy collisions (setting position around ennemy as not safe unless we can chase it (outnumber + high halite value))

## Retreat

Here I determine the distance of all ships to the closest dock.  If this number is greater or equal to the remaining turns left in the game, all ships will be commanded to retreat.  One disadvantage to this is that very close ships to the dock will also be commanded to go home, where it can really harvest more halite.  I didnt get a chance to make this better.

## Priority queue

I'm creating a queue with each ship, ordered by the number of available move.

## Build

Here I determine each ships that are to build docks.  If a ship is reaching an area with significant amount of halite around, and is loaded with halite, it will be define as moving towards the best surrounding spot and build a dropoff. If there exist a dock close by, it will not build a dock.

## Attack

Here ships that are attacking with support.  A lot of these are again based on whatever value is set in the parameter.  It basically determines if a ship attack and potentially dies, could the support ship gain a certain percentage, if so do attack.

## Explore Target

Here I determine the status of each exploring ship. Once an explroing ship with be processed in the queuing list, the following happens: the ship is scanning the surrounding like a radar and as soon as it find a cell with a certain amount of halite (this value will vary during the game, as the average halite with get lower and lower). Once a destination is defined, it is locked and not other ship can go there. Ship that are closest to the target gets priority.

## Deposit

Here ships determined to be depositing from explore target will be moved.  It also include ships that were returning/depositing from the previous turn. If its target cell has a harvest amount thats too much (go over 1000) it will just go towards home.  Depositing ships may harvest while going home, if the cell it steps on has enough halite, based on what value we set the parameter to.  If a ship is close to the enemy and has at least 800 cargo, it will also be commanded to deposit.  I believe the deposit move is the only place where I used A* in determining the path.  Using it with the other movement didnt seem to have that much of an effect, from my testing at least.

## Harvest

Here ships stepping on a cell that has a certain halite, will harvest this turn.

## Explore

Here the remaining ships are moved base on their target.

## Processing the queue

Depending on the amount of move available, we will first process the ships with no actions available (stuck because they can't move), then one move possible, and so on.
Everytime we are done with the group with the lowest number of possible mouvement, we are updating the remaining ships and their amount of mouvement left. This way we are always moving ships as efficiently as possible. 

## Spawn

Here I determine if we are to spawn a ship or not.  It is based only on the amount of Halite left, the number of ships of my opponent  and the turn number we are in. We are stopping spawning at 75 % of the game.

# Regrets/Improvements
* Better workflow. Has a first timer, I'm still happy but there is a lot of improvement to do in the workflow.
* Better algorithm in determining dock locations. It was more a matter of luck (to be a the right place, at the right time) than planning.
* Better 4 player games.  We were creating a lot of ships and sometimes even timeout because of the amount of ships.
* Better attack algorithm.  I notice top players have other ships 'blocking' the enemy so that other ships can harvest the high halite cell. This seems very effective against most players.  Also, some players have an algorithm that surround an enemy, basically cornering it before it collides to it.  This is very efficient, because it prevents the 'chasing' movement that can be very costly.
