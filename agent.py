#########################################
#                                       #
#                                       #
#  ==  SOKOBAN STUDENT AGENT CODE  ==   #
#                                       #
#      Written by: [SHREERAJ PAWAWR]    #
#                                       #
#                                       #
#########################################


# SOLVER CLASSES WHERE AGENT CODES GO
from queue import Queue
from sys import flags
from threading import current_thread
from warnings import catch_warnings
from helper import *
import random
import math

# Base class of agent (DO NOT TOUCH!)
class Agent:
    def getSolution(self, state, maxIterations):

        '''
        EXAMPLE USE FOR TREE SEARCH AGENT:


        #expand the tree until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations or maxIterations <= 0) and len(queue) > 0:
            iterations += 1

            [ POP NODE OFF OF QUEUE ]

            [ EVALUATE NODE AS WIN STATE]
                [ IF WIN STATE: BREAK AND RETURN NODE'S ACTION SEQUENCE]

            [ GET NODE'S CHILDREN ]

            [ ADD VALID CHILDREN TO QUEUE ]

            [ SAVE CURRENT BEST NODE ]


        '''


        '''
        EXAMPLE USE FOR EVOLUTION BASED AGENT:
        #expand the tree until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations or maxIterations <= 0) and len(queue) > 0:
            iterations += 1

            [ MUTATE ]

            [ EVALUATE ]
                [ IF WIN STATE: BREAK AND RETURN ]

            [ SAVE CURRENT BEST ]

        '''


        return []       # set of actions


#####       EXAMPLE AGENTS      #####

# Do Nothing Agent code - the laziest of the agents
class DoNothingAgent(Agent):
    def getSolution(self, state, maxIterations):
        if maxIterations == -1:     # RIP your machine if you remove this block
            return []

        #make idle action set
        nothActionSet = []
        for i in range(20):
            nothActionSet.append({"x":0,"y":0})

        return nothActionSet

# Random Agent code - completes random actions
class RandomAgent(Agent):
    def getSolution(self, state, maxIterations):

        #make random action set
        randActionSet = []
        for i in range(20):
            randActionSet.append(random.choice(directions))

        return randActionSet




#####    ASSIGNMENT 1 AGENTS    #####


# BFS Agent code
class BFSAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None
        queue = [Node(state.clone(), None, None)]
        visited = []

        #expand the tree until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations or maxIterations <= 0) and len(queue) > 0:
    
            iterations += 1

            # YOUR CODE HERE
            # [ POP NODE OFF OF QUEUE ]
            current_node = queue.pop(0)
            if current_node not in visited:
                visited.append(current_node)

            # [ EVALUATE NODE AS WIN STATE]
            # [ IF WIN STATE: BREAK AND RETURN NODE'S ACTION SEQUENCE]
            if current_node.checkWin():
                break            
            # [ GET NODE'S CHILDREN ]
            children_node =  current_node.getChildren()

            children_node_hash = [ node.getHash() for node in children_node]
            queue_node_hash = [ node.getHash() for node in queue]
            visited_node_hash = [ node.getHash() for node in visited ]
            
            # add valid children to
            for i in range(len(children_node)):
                if children_node_hash[i] not in queue_node_hash and children_node_hash[i] not in visited_node_hash:
                    queue.append(children_node[i])

        # [ SAVE CURRENT BEST NODE ]
        bestNode = current_node
        return bestNode.getActions()   #uncomment me



# DFS Agent Code
class DFSAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None
        stack = [Node(state.clone(), None, None)]
        visited = []
        
        #expand the tree until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations or maxIterations <= 0) and len(stack) > 0:
            iterations += 1

            # YOUR CODE HERE
            current_node = stack.pop()
            if current_node not in visited:
                visited.append(current_node)

            # check win condition 
            if current_node.checkWin():
                break

            # get children
            children_node = current_node.getChildren()

            children_node_hash = [ node.getHash() for node in children_node]
            stack_node_hash = [ node.getHash() for node in stack]
            visited_node_hash = [ node.getHash() for node in visited ]
            
            # add valid children to
            for i in range(len(children_node)):
                if children_node_hash[i] not in stack_node_hash and children_node_hash[i] not in visited_node_hash:
                    stack.append(children_node[i])

        bestNode = current_node        
        return bestNode.getActions()   #uncomment me


# AStar Agent Code
class AStarAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None

        #initialize priority queue
        queue = PriorityQueue()
        intial_state = Node(state.clone(), None, None)
        intial_state_cost = intial_state.getHeuristic() + intial_state.getCost()
        queue.put( (intial_state, intial_state_cost) )
        visited = []
        children_node_Totalcost = []

        
        while (iterations < maxIterations or maxIterations <= 0) and queue.qsize() > 0:
            iterations += 1

            ## YOUR CODE HERE ##
            # pop queue
            current_node , _ = queue.get()
            #check win condition
            if current_node.checkWin():
                break

            # get children of first node
            children_node = current_node.getChildren()
            for child in children_node:
                children_node_Totalcost.append( child.getHeuristic() + child.getCost() )


            #getting hashes 
            # deque to a normal queue(list) as Priority Queue are non iteratable
            deque = queue.queue
            children_node_hash = [ node.getHash() for node in children_node]
            visited_node_hash = [ node.getHash() for node in visited ]   
            queue_node_hash = [ node.getHash() for node, _ in deque]
                
            

            # add valid children to queue
            for i in range(len(children_node)):
                if children_node_hash[i] not in queue_node_hash and children_node_hash[i] not in visited_node_hash:
                    queue.put((children_node[i],children_node_Totalcost[i]))

                # to update cost of node preset in the queue
                elif children_node_hash[i] in queue_node_hash:
                    #get child node corresponding to that hash 
                    node = children_node[i]
                    #get total updated cost of that node
                    total_updated = children_node_Totalcost[i]
                    #check if updated cost is less than the cost of node present in queue
                    for i in range(len(deque)):
                        old_node , cost = deque[i] 
                        if old_node == node and total_updated < cost:
                            #remove the node in queue with higher cost and replace it with lower cost 
                            deque.pop(i)
                            queue.put((node,total_updated))
                            

                    

        bestNode = current_node
        print(bestNode.getActions())
        return bestNode.getActions()   






#####    ASSIGNMENT 2 AGENTS    #####


# Hill Climber Agent code
class HillClimberAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)
        iterations = 0
        
        seqLen = 50            # maximum length of the sequences generated
        coinFlip = 0.5          # chance to mutate

        #initialize the first sequence (random movements)
        bestSeq = []
        for i in range(seqLen):
            bestSeq.append(random.choice(directions))
            

        current_state = state.clone()
        for s in bestSeq:
            current_state.update(s['x'],s['y'])

        if current_state.checkWin():
            return bestSeq

        #CALCULATE the base heuristic value of the current state    
        h_min = getHeuristic(current_state)


        #mutate the best sequence until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations):
            iterations += 1
            
            ## YOUR CODE HERE ##
            
            ## making copy of bestSeq
            mutate_bestSeq = bestSeq

            #mutate random directions in BestSeqence 
            for i in range(len(mutate_bestSeq)):        
                if random.random() < coinFlip:
                #mutuate the genome
                    mutate_bestSeq[i] = random.choice(directions)
            
            #make a neighbour based on mutated bestSeq 
            neigh_state = state.clone()
            for s in mutate_bestSeq:
                neigh_state.update(s['x'] , s['y'])    
                  
            #calculate heuristic vale of neighbour state
            h_neigh = getHeuristic(neigh_state)
            if h_neigh < h_min :
                h_min = h_neigh
                bestSeq = mutate_bestSeq
            else:
                continue

            #check for win condition 
            if neigh_state.checkWin():
                break

        #return the best sequence found
        return bestSeq  



# Genetic Algorithm code
class GeneticAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)

        iterations = 0
        seqLen = 50             # maximum length of the sequences generated
        popSize = 10            # size of the population to sample from
        parentRand = 0.5        # chance to select action from parent 1 (50/50)
        mutRand = 0.3           # chance to mutate offspring action

        bestSeq = []            #best sequence to use in case iterations max out

        #initialize the population with sequences of POP_SIZE actions (random movements)
        population = []
        total = 0
        for p in range(popSize):
            total += p
            bestSeq = []
            for _ in range(seqLen):
                bestSeq.append(random.choice(directions))
            population.append(bestSeq)


        #mutate until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations):
            iterations += 1

            #1. evaluate the population
            candiates  = []
            index = 0
            for seq in population:
                new_state = state.clone()
                for s in seq:
                    #print(type(s))
                    new_state.update(s['x'],s['y'])
                h = getHeuristic(new_state)
                candiates.append((seq,h))


            #2. sort the population by fitness (low to high)
            candiates.sort( key= lambda x: x[1])

            

            #2.1 save bestSeq from best evaluated sequence
            bestSeq = candiates[0][0]
            

            #3. generate probabilities for parent selection based on fitness
            
            individuals = list(map(lambda x:x[0] , candiates))
            additive_total = total + popSize
                
            probs = []    
            for i in range(popSize , 0, -1):
                probs.append(i/additive_total)
            #print(probs)

            
                

            #4. populate by crossover and mutation
            new_pop = []
            for i in range(int(popSize/2)):
                #4.1 select 2 parents sequences based on probabilities generated
                par1 = []
                par2 = []

                rand1 = random.random()
                rand2 = random.random()
                sum_probs = 0
                for i,_ in enumerate(candiates):
                    sum_probs += probs[i]
                    if sum_probs > rand1:
                        par1 = candiates[i][0]
                    if sum_probs > rand2:
                        par2 = candiates[i][0]
                    
                
                                
                #4.2 make a child from the crossover of the two parent sequences
                offspring = []
                for i in range(len(par1)):
                    prob = random.random()
                    if prob < parentRand:
                        offspring.append(par1[i])
                    else:
                        offspring.append(par2[i])


                #4.3 mutate the child's actions
                for index, _ in enumerate(offspring):
                    if random.random() < mutRand:
                        offspring[index] = random.choice(directions)
                

                #4.4 add the child to the new population
                new_pop.append(offspring)
           
                
            #5. add top half from last population (mu + lambda)
            new_pop = new_pop + individuals[:5]
            
            
            #6. replace the old population with the new one
            population = list(new_pop)

        #return the best found sequence 
        return bestSeq


# MCTS Specific node to keep track of rollout and score
class MCTSNode(Node):
    def __init__(self, state, parent, action, maxDist):
        super().__init__(state,parent,action)
        self.children = []  #keep track of child nodes
        self.n = 0          #visits
        self.q = 0          #score
        self.maxDist = maxDist      #starting distance from the goal (heurstic score of initNode)

    #update get children for the MCTS
    def getChildren(self,visited):
        #if the children have already been made use them
        if(len(self.children) > 0):
            return self.children

        children = []

        #check every possible movement direction to create another child
        for d in directions:
            childState = self.state.clone()
            crateMove = childState.update(d["x"], d["y"])

            #if the node is the same spot as the parent, skip
            if childState.player["x"] == self.state.player["x"] and childState.player["y"] == self.state.player["y"]:
                continue

            #if this node causes the game to be unsolvable (i.e. putting crate in a corner), skip
            if crateMove and checkDeadlock(childState):
                continue

            #if this node has already been visited (same placement of player and crates as another seen node), skip
            if getHash(childState) in visited:
                continue

            #otherwise add the node as a child
            children.append(MCTSNode(childState, self, d, self.maxDist))

        self.children = list(children)    #save node children to generated child

        return children

    #calculates the score the distance from the starting point to the ending point (closer = better = larger number)
    def calcEvalScore(self,state):
        return self.maxDist - getHeuristic(state)

    #compares the score of 2 mcts nodes
    def __lt__(self, other):
        return self.q < other.q

    #print the score, node depth, and actions leading to it
    #for use with debugging
    def __str__(self):
        return str(self.q) + ", " + str(self.n) + ' - ' + str(self.getActions())


# Monte Carlo Tree Search Algorithm code
class MCTSAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None
        initNode = MCTSNode(state.clone(), None, None, getHeuristic(state))

        if initNode.checkWin():
            return initNode.getActions()

        while(iterations < maxIterations):
            #print("\n\n---------------- ITERATION " + str(iterations+1) + " ----------------------\n\n")
            iterations += 1

            #mcts algorithm
            #print(iterations)


            rollNode = self.treePolicy(initNode)
            score = self.rollout(rollNode)
            self.backpropogation(rollNode, score)

            #if in a win state, return the sequence
            if(rollNode.checkWin()):
                return rollNode.getActions()

            #set current best node
            #print('Second bestchild call')
            bestNode = self.bestChildUCT(initNode)

            #if in a win state, return the sequence
            if(bestNode and bestNode.checkWin()):
                return bestNode.getActions()



        #return solution of highest scoring descendent for best node
        #if this line was reached, that means the iterations timed out before a solution was found
        return self.bestActions(bestNode)
        

    #returns the descendent with the best action sequence based
    def bestActions(self, node):
        #no node given - return nothing
        if node == None:
            return []

        while(len(node.children) > 0):
            node = self.bestChildUCT(node)

        return node.getActions()


    ####  MCTS SPECIFIC FUNCTIONS BELOW  ####

    #determines which node to expand next
    def treePolicy(self, rootNode):
        #print("in tree policy")
        curNode = rootNode
        visited = set()
        ## YOUR CODE HERE ##
        while curNode.checkWin() != True:
            visited.add(curNode.getHash())
            children = curNode.getChildren(visited)
            for child in children:
                if child.n == 0:
                    curNode = child
                    return child
            curNode = self.bestChildUCT(curNode)
        return curNode



    # uses the exploitation/exploration algorithm
    def bestChildUCT(self, node):
        #print("in bestChild")
        c = 1               #c value in the exploration/exploitation equation
        bestChild = node.parent
        minvalue = -99999

        children = node.getChildren(set())
        for child in children:
            #calculating UCB1 value
            if child.n >0:
                exploitation = child.q / child.n
                exploration =   c * math.sqrt( 2 * math.log(node.n) / child.n )
                value = exploitation + exploration
                if value > minvalue:
                    minvalue = value
                    bestChild = child
        return bestChild
    

     #simulates a score based on random actions taken
    def rollout(self,node):
        #print("in rollout")
        numRolls = 7        #number of times to rollout to

        ## YOUR CODE HERE ##
        simulate_state = node.state.clone()
        dir = random.choices(directions, k=numRolls)
        for seq in dir:
            simulate_state.update(seq['x'] , seq['y'])
         
        return node.calcEvalScore(simulate_state)



     #updates the score all the way up to the root node
    def backpropogation(self, node, score):
        #print("in backpropagation")

        ## YOUR CODE HERE ##
        while node != None:
            node.n = node.n + 1
            node.q = node.q + score
            node = node.parent

        

