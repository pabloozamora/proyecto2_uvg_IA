# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()
        currentPos = gameState.getPacmanPosition()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action, currentPos) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        
        '''for currentIndex in bestIndices:
            nextAction = legalMoves[currentIndex]
            gameState.getPacmanNextState(nextAction)'''
            

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action, currentPos):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        ''' --- PROYECTO --- '''
        "*** YOUR CODE HERE ***"
        
        newFoodList = newFood.asList()
        '''print(f'childGameState: {childGameState}')
        print(f'newPos: {newPos}')
        print(f'newFoodList: {newFoodList}')
        print(f'newSacaredTimes: {newScaredTimes}')'''
        
        score = 0
        minDistance = 999999999
        
        for state in newGhostStates:
            if state.scaredTimer == 0 and state.getPosition() == tuple(newPos):
                return -999999999 # Penalizar la acción lleva a la posición de un fantasma
        
        foodDistance = [manhattanDistance(newPos, foodPosition) for foodPosition in newFoodList] # Encontrar la distancia desde PacMan hacia cada comida
        
        if len(foodDistance): # Verificar que la lista de comida faltante no esté vacía (Es decir, que no se ha acabado el juego)
            minDistance = min(foodDistance)
        
        # Proprocionalidad inversa entre el max_score y distancia Manhattan mínima y penalizar las posiciones que se alejan de la comida
        score = (10.0 / minDistance) - 40 * len(foodDistance)
        
        if newPos in newFoodList: score += 10 # Despenalizar si en la siguiente posición se encuentra comida
                
        if newPos == currentPos: score -= 100 # Penalizar regresar a la posición anterior (Evitar ciclos)

        if action == 'Stop':
            score -= 20 # Penalizar la acción Stop
        
        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        ''' --- PROYECTO --- '''
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        bestAction = self.maxScore(gameState=gameState, depth=0, agentIndex=0)[1]
        return bestAction
        
    def isTerminalState(self, gameState, depth, agentIndex):
        
        '''Función helper para determinar si el nodo actual del árbol es terminal'''
        
        if gameState.isWin(): return gameState.isWin()
        elif gameState.isLose(): return gameState.isLose()
        elif len(gameState.getLegalActions(agentIndex)) == 0: return True
        elif depth >= self.depth * gameState.getNumAgents(): return True # self.depth cuenta como un movimiento de PacMan y cada fantasma, por lo que se multiplica por el numAgents
        
    def maxScore(self, gameState, depth, agentIndex):
        
        '''Función helper para determinar el máximo valor posible de un nodo'''
        
        max_score = (-999999, None)
        legalActions = gameState.getLegalActions(agentIndex) # Obtener las posibles acciones para el agente actual
        for action in legalActions:
            childGameState = gameState.getNextState(agentIndex, action) # Obtener el siguiente estado del juego
            numAgents = gameState.getNumAgents()
            nextDepth = depth + 1 # Expandir al siguiente nivel de profunidad
            nextAgent = nextDepth % numAgents # Determinar el agente según el nivel de profundidad
            max_score = max([max_score, (self.minimax(childGameState, nextDepth, nextAgent), action)], key=lambda index: index[0]) # Recursividad para obtener el máximo valor posible en el nodo actual
        
        return max_score
    
    def minScore(self, gameState, depth, agentIndex):
        
        '''Función helper para determinar el mínimo valor posible de un nodo'''
        
        min_score = (999999, None)
        legalActions = gameState.getLegalActions(agentIndex) # Obtener las posibles acciones para el agente actual
        for action in legalActions:
            childGameState = gameState.getNextState(agentIndex, action) # Obtener el siguiente estado del juego
            numAgents = gameState.getNumAgents()
            nextDepth = depth + 1 # Expandir al siguiente nivel de profunidad
            nextAgent = nextDepth % numAgents # Determinar el agente según el nivel de profundidad
            min_score = min([min_score, (self.minimax(childGameState, nextDepth, nextAgent), action)], key=lambda index: index[0]) # Recursividad para obtener el máximo valor posible en el nodo actual
        
        return min_score
    
    def minimax(self, gameState, depth, agentIndex):
        
        ''' Función recursiva que determina si se debe calcular el máximo posible o mínimo posible dependiendo del agente (o regresar la utilidad en caso se trate de un nodo terminal) '''    
        
        if self.isTerminalState(gameState, depth, agentIndex): # Si se trata de un nodo terminal, devolver el score
            return self.evaluationFunction(gameState)
        
        elif agentIndex == 0: # Si se trata de PacMan, determinar la máxima utilidad para el nodo actual
            return self.maxScore(gameState, depth, agentIndex)[0]
        
        else: # Si se trata de un fantasma, determinar la mínima utilidad para el nodo actual
            return self.minScore(gameState, depth, agentIndex)[0]
        
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()    

# Abbreviation
better = betterEvaluationFunction
