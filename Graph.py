class Graph:
    """
    A dictionary of the states in the graph with functions for adding vertices and edges. Handles parsed input to build graph.

    ...

    Attributes
    ----------
    states : dict[str, Graph.State]
        The states in the graph. Key is the state name, value is the state itself.

    Methods
    -------
    addStatesAndEdge(state1, state2, cost)
        Add state1 and state2 if not present and add the edge between them.
    setHeuristic(state, heuristic)
        Set the heuristic value for the state with the given stateName.
    getState(name)
        Return the State with the given name.
    """

    states : dict 
    def __init__(self):
        self.states = {}
    def addStatesAndEdge(self, state1, state2, cost):
        """
        Add states for state1 and state2 if they do not already exist in the graph and add an edge between them.

        Parameters
        ----------
        state1 : str
            The name of one state.
        state2 : str
            The name of a state adjacent to state1.
        cost : float
            The cost of the edge between state1 and state2.
        """

        if (state1 not in self.states):
            self.states[state1] = State(state1)
        if (state2 not in self.states):
            self.states[state2] = State(state2)
        self.states[state1].addEdges(self.states[state2], cost)
    def setHeuristic(self, stateName, heuristic):
        """
        Set the heuristic for the given state.

        Parameters
        ----------
        stateName : str
            The name of the state to set the heuristic for
        heuristic : float
            The (under)estimated distance to the goal state of the graph.
        """

        self.states[stateName].setHeuristic(heuristic)
    def getState(self, name):
        """
        Return the state with the given name.

        Parameters
        ----------
        name : str
            The name of the state to return.
        """

        return self.states[name]
class State:
    """
    The structure for a vertex with edges as a property.

    ...

    Attributes
    ----------
    name : str
        String identifier for this state.
    heuristic : float
        The (under)estimated distance from this state to the goal state of the graph.
    edges : dict
        A dictionary relating the names of the adjacent states to the respective path cost from itself to this state.

    Methods
    -------
    setHeuristic(heuristic)
        Set the heuristic value associated with this state.
    addEdges(otherState, cost)
        Add a bi-directional edge between this state and otherState with the given cost.
    """
    name : str
    heuristic : float
    edges : dict  
    def __init__(self, name):
        """
        Constructor for a State object. Does not create edges.

        Parameters
        ----------
        name : str
            The string value of the vertex. One capital letter, not enforced by this method.
        """

        self.name = name
        self.heuristic = 0
        self.edges = {}
    def setHeuristic(self, heuristic):
        """
        heuristic : float
            The (under)estimated distance to the goal state of the graph.
        """
        
        self.heuristic = heuristic
    def addEdges(self, otherState, cost):
        """
        Add an edge from this state to otherState and from otherState to this state since all edges are bi-directional.

        Parameters
        ----------
        otherState : State
            The state to add a bi-directional edge to this state.
        cost : float
            The cost of the edge being added.
        """

        self.edges[otherState.name] = cost
        otherState.edges[self.name] = cost

