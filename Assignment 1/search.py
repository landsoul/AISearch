# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    "initialize the frontier using the initial state of problem"
    frontier = util.Stack()
    start = (problem.getStartState(), [], 0)
    frontier.push(start)

    "initialize the explored set to be empty"
    explored = []
    # loop(do if (the frontier is empty then(
    while True:
        if frontier.isEmpty():
            return []
        # choose a node and remove it from the frontier
        else:
            current = frontier.pop()
            # if (the node contains a goal state then
            if problem.isGoalState(current[0]):
                return current[1]
            else:
                # else add the node to the explored set
                explored.append(current[0])
                # expand the chosen node, adding all the neighboring nodes to the frontier
                # but only if the child is not already in the explored set
                for node in problem.getSuccessors(current[0]):
                    if node[0] not in explored:
                        # make the directions into a list, and add costs before pushing to stack.
                        frontier.push((node[0], current[1] + [node[1]], current[2] + node[2]))

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    start = (problem.getStartState(), [], 0)
    frontier.push(start)

    "initialize the explored set to be empty"
    explored = []
    expanded = []
    # loop(do if (the frontier is empty then(
    while True:
        if frontier.isEmpty():
            return []
        # choose a node and remove it from the frontier
        else:
            current = frontier.pop()
            # if (the node contains a goal state then
            if problem.isGoalState(current[0]):
                print("Goal State:", current)
                print("cost of solution:", current[2])
                return current[1]
            else:
                # else add the node to the explored set
                if current[0] not in explored:
                    explored.append(current[0])
                # expand the chosen node, adding all the neighboring nodes to the frontier
                # but only if the child is not already in the explored set
                for node in problem.getSuccessors(current[0]):
                    if node[0] not in explored and node[0] not in expanded:
                        # make the directions into a list, and add costs before pushing to stack.
                        # new_node = (node[0], current[1] + [node[1]], current[2] + node[2])
                        # print(new_node)
                        frontier.push((node[0], current[1] + [node[1]], current[2] + node[2]))
                        expanded.append(node[0])  # preventing duplicate expansions


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    start = (problem.getStartState(), [], 0)
    frontier.push(start, 0)

    explored = []
    expanded = []
    while True:
        if frontier.isEmpty():
            return []
        else:
            current = frontier.pop()
            if problem.isGoalState(current[0]):
                return current[1]
            else:
                # else add the node to the explored set
                if current[0] not in explored:
                    explored.append(current[0])
                # expand the chosen node, adding all the neighboring nodes to the frontier
                # but only if the child is not already in the explored set
                for node in problem.getSuccessors(current[0]):
                    if node[0] not in explored:
                        # expanding to a goal state multiple times is fine.
                        if problem.isGoalState(node[0]) or node[0] not in expanded:
                            total_cost = current[2] + node[2]
                            frontier.push((node[0], current[1] + [node[1]], total_cost), total_cost)
                            expanded.append(node[0])  # preventing duplicate expansions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    start = (problem.getStartState(), [], 0)
    heu = heuristic(problem.getStartState(), problem)
    frontier.push(start, start[2] + heu)

    explored = []
    expanded = []

    explored.append((start[0], start[2] + heu))

    while True:
        if frontier.isEmpty():
            return []
        else:
            current = frontier.pop()
            if problem.isGoalState(current[0]):
                return current[1]
            else:
                # else add the node to the explored set
                if current[0] not in explored:
                    explored.append(current[0])
                # expand the chosen node, adding all the neighboring nodes to the frontier
                # but only if the child is not already in the explored set

                for node in problem.getSuccessors(current[0]):
                    heu = heuristic(node[0], problem)
                    total_cost = current[2] + node[2]
                    total_heu_cost = total_cost + heu
                    if node[0] not in explored[0]:
                        # add it to the explored set
                        # print(node[0], heu)
                        explored.append((node[0], node[2] + heu))
                        # check its heuristic & add it to a list
                        # expanding to a goal state multiple times is fine.
                        if problem.isGoalState(node[0]) or node[0] not in expanded:
                            # print("node to expand ->", node[0], "Cost of ->", total_cost)
                            frontier.push((node[0], current[1] + [node[1]], total_cost), total_heu_cost)
                            expanded.append(node[0])  # preventing duplicate expansions

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
