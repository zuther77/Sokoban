################################################
#                                              #
#     LEVEL GENERATOR FOR SOKOBAN FRAMEWORK    #
#         Written by [SHREERAJ PAWAR ]         #
#                                              #
################################################


# import libraries
import numpy as np
import random
from agent import DoNothingAgent, RandomAgent, BFSAgent, DFSAgent, AStarAgent, HillClimberAgent, GeneticAgent, MCTSAgent
from helper import *
import os

# COMMAND LINE ARGS
EVAL_AGENT = "AStar"			#sokoban master agent to use as evaluator
SOLVE_ITERATIONS = 1250			#number of iterations to run agent for

MIN_SOL_LEN = 5					#minimum length of solution
MAX_SOL_LEN = 25				#maximum length of solution

NUM_LEVELS = 20					#number of levels to generate
OUT_DIR = "assets/gen_levels"	#directory to output generated levels
LEVEL_PREFIX = "Level"			#prefix for the filename of the generated levels


# SOKOBAN ASCII CHARS KEY #
_player = "@"  #1 per game
_crate = "$"
_wall = "#"
_floor = " "
_emptyGoal = "."
_filledGoal = "*"


#turns 2d array of a level into an ascii string
def lev2Str(l):
	s = ""
	for r in l:
		s += ("".join(r) + "\n")
	return s









# creates an empty base sokoban level
def makeEmptyLevel(w=9,h=9):
	l = []

	tbw = [] #top/bottom walls
	lrw = [] #left/right walls

	#initialize row setup
	for i in range(w):
		tbw.append(_wall)
	for i in range(w):
		if i == 0 or i == (w-1):
			lrw.append(_wall)
		else:
			lrw.append(_floor)

	#make level
	for i in range(h):
		if i == 0 or i == (h-1):
			l.append(tbw[:])
		else:
			l.append(lrw[:])

	return l






###############################
##                           ##
##      ADD YOUR HELPER      ##
##      FUNCTIONS HERE       ##
##                           ##
###############################


def push_start(l,a,b):
	#choose a random point to start within the box
	while True:
		x = random.randint(1,a)
		y = random.randint(1,b)
		#if there is a wall already there choose different point 
		if l[x][y] == _wall:
			x = random.randint(1,a)
			y = random.randint(1,b)
		else:
			break
	l[x][y] = _player
	return l
	



def base(h):
	return [_wall] * h


def addboundry(level):
	width = len(level) 
	height = len(level) + 2

	temp = [ _wall for i in range(width+1)]
	#print(temp)
	
	for i in range(height):
		if i == 0 or i == height -1:
			level.insert(i,temp)
		else:
			#level[i].insert(0,_wall)
			level[i].insert(width,_wall)
	
	level.insert(height,temp)
	return level

def add_boxes_add_goals(level, boxes):
	goals = boxes 
	#print("Goals : " ,goals)
	'''we add boxes first
	logic - 
	1) get all the floor indexes from the level and store in list
	2) choose a random index
	3) check if there is not more that 3 walls in all 8 directions
	4) check if there is no box within 2 spaces of each other
	5) if such index exits place box and decrement number of boxes
	6) delete entries for the index where box placed 
	7) repeat 2-6 till number of goals = 0
	'''

	#step 1 ( top left point is [0,0])
	indexes = [(x,y) for x,row in enumerate(level) for y in range(len(row)) if row[y]==_floor ]
	#print(len(indexes))

	#checking neighbour logic 
	while boxes:
		wall_count = 0
		x ,y = random.choice(indexes)
		
		#check left
		if level[x][y-1] == _wall:
			#print("wall")
			wall_count +=1
		#check left
		if level[x][y+1] == _wall:
			#print("wall")
			wall_count +=1
		#check top
		if level[x-1][y] == _wall:
			#print("wall")
			wall_count +=1
		#check bottom
		if level[x+1][y] == _wall:
			#print("wall")
			wall_count +=1
		#check bottom left 
		if level[x+1][y-1] == _wall:
			wall_count +=1
		#check bottom right
		if level[x+1][y+1] == _wall:
			wall_count +=1
		#check top left 
		if level[x-1][y-1] == _wall:
			wall_count +=1
		#check bottom right
		if level[x-1][y+1] == _wall:
			wall_count +=1
		

		if wall_count < 3 :
			level[x][y] = _crate
			indexes.remove((x,y))
			boxes -= 1
		
	#print(len(indexes))


	'''
	now we add goals
	logic- 
	1) use the updated index list from above
	2) randomly place goals 
	'''
	while goals:
		x,y = random.choice(indexes)
		if level[x][y] == _floor:
			level[x][y] = _emptyGoal
			goals -= 1

	return level


#generates a level
def buildALevel():
	# WRITE YOUR OWN CODE HERE
	#declare some constants
	WIDHTH = HEIGHT = 9
	_number_boxes_ = 2

	#l= makeEmptyLevel()  # needs to be a 2d char array (use the characters from the key above)

	l = [ base(HEIGHT) for _ in range(WIDHTH)]
	# WRITE YOUR CODE HERE #

	#we begin by chosing a random point within the boundry box
	# width -2 , height - 2

	drunk = { 
		'wallcounter' : (HEIGHT-2) * (WIDHTH-2),
		'boundry' : 1,
		'x' : int(WIDHTH/2),
		'y' : int(HEIGHT/2)
	}

	while drunk["wallcounter"] >=0:
		x = drunk["x"]
		y = drunk["y"]

		prob = random.random()
		if l[x][y] == _wall:
			prob1 = random.random()
			if prob1 > prob:
				l[x][y] = _floor
				drunk["wallcounter"] -= 1

		num = random.randint(1,4)

		if num == 1 and x> drunk["boundry"]:
			drunk["x"] -= 1

		if num == 2 and x< WIDHTH -drunk["boundry"]:
			drunk["x"] += 1	
		
		if num == 3 and y> drunk["boundry"]:
			drunk["y"] -=1

		if num == 4 and y< HEIGHT -drunk["boundry"]:
			drunk["y"] +=1

	l = push_start(l,WIDHTH-drunk["boundry"],HEIGHT - drunk["boundry"])
	l = addboundry(l)
	l = add_boxes_add_goals(l, _number_boxes_)


	return lev2Str(l)  #returns as a string









#use the agent to attempt to solve the level
def solveLevel(l,bot):
	#create new state from level
	state = State()
	state.stringInitialize(l.split("\n"))

	#evaluate level
	sol = bot.getSolution(state, maxIterations=SOLVE_ITERATIONS)
	for s in sol:
		state.update(s['x'],s['y'])
	return state.checkWin(), len(sol)


#generate and export levels using the PCG level builder and agent evaluator
def generateLevels():
	#set the agent
	if EVAL_AGENT == 'DoNothing':
		solver = DoNothingAgent()
	elif EVAL_AGENT == 'Random':
		solver = RandomAgent()
	elif EVAL_AGENT == 'BFS':
		solver = BFSAgent()
	elif EVAL_AGENT == 'DFS':
		solver = DFSAgent()
	elif EVAL_AGENT == 'AStar':
		solver = AStarAgent()
	elif EVAL_AGENT == 'HillClimber':
		solver = HillClimberAgent()
	elif EVAL_AGENT == 'Genetic':
		solver = GeneticAgent()
	elif EVAL_AGENT == 'MCTS':
		solver = MCTSAgent()

	#create the directory if it doesn't exist
	if not os.path.exists(OUT_DIR):
		os.makedirs(OUT_DIR)

	#create levels
	totLevels = 0
	while totLevels < NUM_LEVELS:
		lvl = buildALevel()
		#print(lvl)
		solvable, solLen = solveLevel(lvl,solver)
	# 	print( solvable , solLen)
	# 	if solvable == True:
	# 		totLevels += 1
	# print("total Solved - ",totLevels)

	# return

		# #uncomment these lines if you want to see all the generated levels (including the failed ones)
		# '''
		# print(f"{lvl}solvable: {solvable}")
		# if solvable:
		# 	print(f"  -> solution len: {solLen}\n")
		# else:
		# 	print("")
		# '''

		#export the level if solvable 
		if solvable and solLen >= MIN_SOL_LEN and solLen <= MAX_SOL_LEN:
			with open(f"{OUT_DIR}/{LEVEL_PREFIX}_{totLevels}.txt",'w') as f:
				f.write(lvl)
			totLevels+=1

			#show the level exported
			print(f"LEVEL #{totLevels}/{NUM_LEVELS} -> {solLen} MOVES\n{lvl}")



#run whole script to generate 
if __name__ == "__main__":
	generateLevels()



