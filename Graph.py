class Graph:
    """
    A dictionary of the nodes in the graph with functions for adding vertices and edges. Handles parsed input to build graph.

    ...

    Attributes
    ----------
    nodes : dict[str, Graph.Node]
        The nodes in the graph. Key is the node name, value is the node itself.

    Methods
    -------
    addNodesAndEdge(node1, node2, cost)
        Add node1 and node2 if not present and add the edge between them.
    setHeuristic(node, heuristic)
        Set the heuristic value for the node with the given nodeName.
    getState(name)
        Return the Node with the given name.
    """

    nodes : dict 
    def __init__(self):
        self.nodes = {}
    def addNodesAndEdge(self, node1 : str, node2 : str, cost : float):
        """
        Add nodes for node1 and node2 if they do not already exist in the graph and add an edge between them.

        Parameters
        ----------
        node1 : str
            The name of one node.
        node2 : str
            The name of a node adjacent to node1.
        cost : float
            The cost of the edge between node1 and node2.
        """

        if (node1 not in self.nodes):
            self.nodes[node1] = Node(node1)
        if (node2 not in self.nodes):
            self.nodes[node2] = Node(node2)
        self.nodes[node1].addEdges(self.nodes[node2], cost)
    def setHeuristic(self, nodeName : str, heuristic : float):
        """
        Set the heuristic for the given node.

        Parameters
        ----------
        nodeName : str
            The name of the node to set the heuristic for
        heuristic : float
            The (under)estimated distance to the goal node of the graph.
        """

        self.nodes[nodeName].setHeuristic(heuristic)
    def getState(self, name : str):
        """
        Return the node with the given name.

        Parameters
        ----------
        name : str
            The name of the node to return.
        """

        return self.nodes[name]
class Node:
    """
    The structure for a vertex with edges as a property.

    ...

    Attributes
    ----------
    name : str
        String identifier for this node.
    heuristic : float
        The (under)estimated distance from this node to the goal node of the graph.
    edges : dict
        A dictionary relating the names of the adjacent nodes to the respective path cost from itself to this node.

    Methods
    -------
    setHeuristic(heuristic)
        Set the heuristic value associated with this node.
    addEdges(otherNode, cost)
        Add a bi-directional edge between this node and otherNode with the given cost.
    """
    name : str
    heuristic : float
    edges : dict  
    def __init__(self, name : str):
        """
        Constructor for a Node object. Does not create edges.

        Parameters
        ----------
        name : str
            The string value of the vertex. One capital letter, not enforced by this method.
        """

        self.name = name
        self.heuristic = 0
        self.edges = {}
    def setHeuristic(self, heuristic : float):
        """
        heuristic : float
            The (under)estimated distance to the goal node of the graph.
        """
        
        self.heuristic = heuristic
    def addEdges(self, otherNode, cost : float):
        """
        Add an edge from this node to otherNode and from otherNode to this node since all edges are bi-directional.

        Parameters
        ----------
        otherNode : Node
            The node to add a bi-directional edge to this node.
        cost : float
            The cost of the edge being added.
        """

        self.edges[otherNode.name] = cost
        otherNode.edges[self.name] = cost

