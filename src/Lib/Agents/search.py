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


def depthFirstSearch(problem: SearchProblem):
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

    # initialize start state
    start = problem.getStartState()
    stack = util.Stack()
    visited = set()
    stack.push((start, []))

    
    while not stack.isEmpty():
        state, path = stack.pop()

        # we found the goal
        if problem.isGoalState(state):
            return path

        # we havent seen this state yet
        if state not in visited:
            visited.add(state)

            # search all the successors
            for successor in problem.getSuccessors(state):
                if successor in visited: # skip the ones weve already seen
                    continue
                stack.push((successor[0], path + [successor[1]]))            


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    # initialize start state
    start = problem.getStartState()
    queue = util.Queue()
    visited = set()
    queue.push((start, []))

    
    while not queue.isEmpty():
        state, path = queue.pop()

        # we found the goal
        if problem.isGoalState(state):
            return path

        # we havent seen this state yet
        if state not in visited:
            visited.add(state)

            # search all the successors
            for successor in problem.getSuccessors(state):
                if successor in visited: # skip the ones weve already seen
                    continue
                queue.push((successor[0], path + [successor[1]]))


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""

    # initialize start state
    start = problem.getStartState()
    queue = util.PriorityQueue()
    visited = set()
    queue.push((start, [], 0), 0)

    
    while not queue.isEmpty():
        state, path, cost = queue.pop()

        # we found the goal
        if problem.isGoalState(state):
            return path

        # we havent seen this state yet
        if state not in visited:
            visited.add(state)

            # search all the successors
            for successor in problem.getSuccessors(state):

                if successor in visited: # skip the ones weve already seen
                    continue

                queue.push((successor[0], path + [successor[1]], cost + successor[2]), cost + successor[2])


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    # initialize start state
    start = problem.getStartState()
    queue = util.PriorityQueue()
    visited = set()
    queue.push((start, [], heuristic(start, problem)), heuristic(start, problem))

    
    while not queue.isEmpty():
        state, path, cost = queue.pop()

        # we found the goal
        if problem.isGoalState(state):
            return path

        # we havent seen this state yet
        if state not in visited:
            visited.add(state)

            # search all the successors
            for successor in problem.getSuccessors(state):
                
                if successor in visited: # skip the ones weve already seen
                    continue

                cumCost = cost + successor[2] + heuristic(successor[0], problem)
                queue.push((successor[0], path + [successor[1]], cost + successor[2]), cumCost)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch