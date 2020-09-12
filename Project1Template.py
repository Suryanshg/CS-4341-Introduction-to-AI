from SearchEnum import SearchEnum
import Graph
import sys
from collections import OrderedDict
# Template for Project 1 of CS 4341 - A2020

class Path:
    """
    A data structure representing paths using nodes and f(n)
    ...

    Attributes
    ----------
    nodes : list[Graph.State]
        The nodes in the path. 
    fn : float
        represents the cost of the path 
    Methods
    -------
    setCost(cost)
        Set the fn value for the path with the given cost.
    getPath()
        Return the nodes in the form of a list
    addNode(node)
        Adds a given node to the path
    """

   
    def __init__(self):
        self.nodes = []
        self.fn=0.0
    
    def setCost(self,cost):
        """
        Set the fn value for the path with the given cost.

        Parameters
        ----------
       cost : float
             cost represents the new value for fn
        """

        self.fn=cost

    def getPath(self):
        """
        Return the list of nodes in the path.
        """
        return self.nodes

    def addNode(self,node):
        """
        Adds a given node to the path

        Parameters
        ----------
       node : Graph.State
             represents a vertex in the Graph
        """
        self.nodes.insert(0,node)

def General_Search(problem, searchMethod):
    """
    Return the solution path or failure to reach state G from state S. 
    
    Parameters
    ----------
    problem : Graph.Graph
        The graph to search from S to G.
    searchMethod : SearchEnum
        The search method to use to search the graph.
    """
    initialState = 'S' # name of the initial state
    finalState = 'G' # Name of the final state
    informedSearchAlgos=[SearchEnum.UNIFORM_COST_SEARCH, SearchEnum.GREEDY_SEARCH, SearchEnum.A_STAR, SearchEnum.HILL_CLIMBING, SearchEnum.BEAM_SEARCH ]
    # Make_Queue, Make_Queue_Node, Remove_Front, Terminal_State, Expand, and expand_queue are to be implemented by the student. 
    # Implementation of the below pseudocode may vary slightly depending on the data structures used.
    L=0 # Variable Limit for IDS 
    queue = Make_Queue(Make_Queue_Node(problem.getState(initialState))) # Initialize the data structures to start the search at initialState
    if(searchMethod in informedSearchAlgos):
        if(searchMethod==SearchEnum.UNIFORM_COST_SEARCH):
            printQueue(queue, True)
        else:
            queue[0].fn = hn(queue[0])
            printQueue(queue, True)
    else:
        printQueue(queue, False)
    while len(queue) > 0:  
        node = Remove_Front(queue) # Remove and return the node to expand from the queue
        if Terminal_State(node) == finalState: # solution is not a defined variable, but this statement represents checking whether you have expanded the goal node.
            return node # If this is a solution, return the node containing the path to reach it.
        opened_nodes = Expand(problem, node) # Get new nodes to add to the queue based on the expanded node.
        #printQueue(opened_nodes)
        queue=expand_queue(queue,opened_nodes,problem,searchMethod, L)
        if (len(queue)==0 and searchMethod == SearchEnum.ITERATIVE_DEEPENING_SEARCH): #If unsuccessful on IDS
            L+=1
            print("\n") 
            queue=Make_Queue(Make_Queue_Node(problem.getState(initialState)))
            printQueue(queue, False)    
    return False

def expand_queue(queue, nodesToAddToQueue, problem, searchMethod, limit):
    """
    Add the new nodes created from the opened nodes to the queue based on the search strategy.

    Parameters
    ----------
    queue 
        The queue containing the possible nodes to expand upon for the search.
    newNodesToAddToQueue : list
        The list of nodes to add to the queue.
    problem : Graph.Graph
        The graph to search from S to G.
    searchMethod : SearchEnum
        The search method to use to search the graph.
    """
    newQueue=[]
    #Fill in the below if and elif bodies to implement how the respective searches add new nodes to the queue.
    if searchMethod == SearchEnum.DEPTH_FIRST_SEARCH:        
        nodesToAddToQueue.extend(queue)
        newQueue=nodesToAddToQueue

        if (len(newQueue)!=0):
            printQueue(newQueue, False)
        
    elif searchMethod == SearchEnum.BREADTH_FIRST_SEARCH:
        queue.extend(nodesToAddToQueue)
        newQueue=queue

        if (len(newQueue)!=0):
            printQueue(newQueue, False)

    elif searchMethod == SearchEnum.DEPTH_LIMITED_SEARCH:
        pathsToRemove=[]
        for path in nodesToAddToQueue:
            if (len(path.nodes)>3): # discard those paths whose depth is greater than 2 + 1
                pathsToRemove.append(path)
        for path in pathsToRemove:
            nodesToAddToQueue.remove(path)
        nodesToAddToQueue.extend(queue)
        newQueue=nodesToAddToQueue

        if (len(newQueue)!=0):
            printQueue(newQueue, False)


    elif searchMethod == SearchEnum.ITERATIVE_DEEPENING_SEARCH:
        pathsToRemove=[]
        i=limit
        for path in nodesToAddToQueue:
            if (len(path.nodes)>i+1): # discard those paths whose depth is greater than 2 + 1
                pathsToRemove.append(path)
        for path in pathsToRemove:
            nodesToAddToQueue.remove(path)
        nodesToAddToQueue.extend(queue)
        newQueue=nodesToAddToQueue

        if (len(newQueue)!=0):
            printQueue(newQueue, False)

    elif searchMethod == SearchEnum.UNIFORM_COST_SEARCH:
        for path in nodesToAddToQueue: # Set the f(n) for all paths
            path.fn=gn(path) # f(n) = g(n) for Uniform Cost Search
        
        for path in nodesToAddToQueue: # Adding children path to the main queue in order
            inserted=False
            for i in range(len(queue)):    
                if(path.fn < queue[i].fn): # if child path has different annd less f(n) then it goes inside first
                    queue.insert(i,path)
                    inserted=True
                    break
                elif(path.fn == queue[i].fn): # the two paths have same value
                    if(path.nodes[0].name != queue[i].nodes[0].name): # If the two paths end at different nodes 
                        if(path.nodes[0].name < queue[i].nodes[0].name): # child path's node is alphabetically first, then insert it before the existing queue
                            queue.insert(i,path)
                            inserted=True
                            break
                    elif(path.nodes[0].name == queue[i].nodes[0].name): # If the two paths end at the same node
                        if(len(path.nodes) != len(queue[i].nodes)): # If the two paths have different length
                            if(len(path.nodes) < len(queue[i].nodes)): # Put in the child path with the shortest length first
                                queue.insert(i,path)
                                inserted=True
                                break
                        else: # The two paths have same length and end at same node     
                            for j in range(1,len(path.nodes)): # Sorting in Lexicographic order
                                if(path.nodes[j] < queue[i].nodes[j]):
                                    queue.insert(i, path)
                                    inserted=True
                                    break
                            break
            if(not inserted): # Should come at the end
                queue.append(path)
        newQueue=queue

        if (len(newQueue)!=0):
            printQueue(newQueue, True)
            

    elif searchMethod == SearchEnum.GREEDY_SEARCH:
        for path in nodesToAddToQueue: # Set the f(n) for all paths
            path.fn=hn(path) # f(n) = h(n) for Greedy Search
        
        for path in nodesToAddToQueue: # Adding children path to the main queue in order
            inserted=False
            for i in range(len(queue)):    
                if(path.fn < queue[i].fn): # if child path has different annd less f(n) then it goes inside first
                    queue.insert(i,path)
                    inserted=True
                    break
                elif(path.fn == queue[i].fn): # the two paths have same value
                    if(path.nodes[0].name != queue[i].nodes[0].name): # If the two paths end at different nodes 
                        if(path.nodes[0].name < queue[i].nodes[0].name): # child path's node is alphabetically first, then insert it before the existing queue
                            queue.insert(i,path)
                            inserted=True
                            break
                    elif(path.nodes[0].name == queue[i].nodes[0].name): # If the two paths end at the same node
                        if(len(path.nodes) != len(queue[i].nodes)): # If the two paths have different length
                            if(len(path.nodes) < len(queue[i].nodes)): # Put in the child path with the shortest length first
                                queue.insert(i,path)
                                inserted=True
                                break
                        else: # The two paths have same length and end at same node     
                            for j in range(1,len(path.nodes)): # Sorting in Lexicographic order
                                if(path.nodes[j] < queue[i].nodes[j]):
                                    queue.insert(i, path)
                                    inserted=True
                                    break
                            break
            if(not inserted): # Should come at the end
                queue.append(path)
        newQueue=queue

        if (len(newQueue)!=0):
            printQueue(newQueue, True)

    elif searchMethod == SearchEnum.A_STAR:
        for path in nodesToAddToQueue: # Set the f(n) for all paths
            path.fn = gn(path) + hn(path) # f(n) = g(n) + h(n) for A* search
        
        for path in nodesToAddToQueue: # Adding children path to the main queue in order
            inserted=False
            for i in range(len(queue)):    
                if(path.fn < queue[i].fn): # if child path has different annd less f(n) then it goes inside first
                    queue.insert(i,path)
                    inserted=True
                    break
                elif(path.fn == queue[i].fn): # the two paths have same value
                    if(path.nodes[0].name != queue[i].nodes[0].name): # If the two paths end at different nodes 
                        if(path.nodes[0].name < queue[i].nodes[0].name): # child path's node is alphabetically first, then insert it before the existing queue
                            queue.insert(i,path)
                            inserted=True
                            break
                    elif(path.nodes[0].name == queue[i].nodes[0].name): # If the two paths end at the same node
                        if(len(path.nodes) != len(queue[i].nodes)): # If the two paths have different length
                            if(len(path.nodes) < len(queue[i].nodes)): # Put in the child path with the shortest length first
                                queue.insert(i,path)
                                inserted=True
                                break
                        else: # The two paths have same length and end at same node     
                            for j in range(1,len(path.nodes)): # Sorting in Lexicographic order
                                if(path.nodes[j] < queue[i].nodes[j]):
                                    queue.insert(i, path)
                                    inserted=True
                                    break
                            break
            if(not inserted): # Should come at the end
                queue.append(path)
        newQueue=queue

        if (len(newQueue)!=0):
            printQueue(newQueue, True)

    elif searchMethod == SearchEnum.HILL_CLIMBING:
        for path in nodesToAddToQueue: # Set the f(n) for all paths
            path.fn = hn(path) # f(n) = h(n) for Hill Climbing Search 

        # for path in nodesToAddToQueue: # Adding children path to the main queue in order
        #     inserted=False
        #     for i in range(len(queue)):    
        #         if(path.fn < queue[i].fn): # if child path has different annd less f(n) then it goes inside first
        #             queue.insert(i,path)
        #             inserted=True
        #             break
        #         elif(path.fn == queue[i].fn): # the two paths have same value
        #             if(path.nodes[0].name != queue[i].nodes[0].name): # If the two paths end at different nodes 
        #                 if(path.nodes[0].name < queue[i].nodes[0].name): # child path's node is alphabetically first, then insert it before the existing queue
        #                     queue.insert(i,path)
        #                     inserted=True
        #                     break
        #             elif(path.nodes[0].name == queue[i].nodes[0].name): # If the two paths end at the same node
        #                 if(len(path.nodes) != len(queue[i].nodes)): # If the two paths have different length
        #                     if(len(path.nodes) < len(queue[i].nodes)): # Put in the child path with the shortest length first
        #                         queue.insert(i,path)
        #                         inserted=True
        #                         break
        #                 else: # The two paths have same length and end at same node     
        #                     for j in range(1,len(path.nodes)): # Sorting in Lexicographic order
        #                         if(path.nodes[j] < queue[i].nodes[j]):
        #                             queue.insert(i, path)
        #                             inserted=True
        #                             break
        #                     break
        #     if(not inserted): # Should come at the end
        #         queue.append(path)
       

        bestPath=Path()
        bestPath.fn = 11.0
        for path in nodesToAddToQueue:
            if(path.fn < bestPath.fn):
                bestPath = path

        newQueue.append(bestPath)

        if (len(newQueue)!=0):
            printQueue(newQueue, True)


    # elif searchMethod == SearchEnum.BEAM_SEARCH:
    
    return newQueue

def Make_Queue(path):
    """
    Returns a queue with the path inserted

    Parameters
    ----------
    path : Path
        Represents the path
    """  
    Q=[path]
    return Q

def Make_Queue_Node(node):
    """
    Returns a Path with the node inserted

    Parameters
    ----------
    node : Graph.State
        The vertex representing the node
    """   
    path = Path()
    path.addNode(node)
    return path

def Remove_Front(queue):
    """
    Returns a path popped out from the front of queue

    Parameters
    ----------
    queue : list of Path
        The list representing the paths
    """   
    returnedPath=queue.pop(0)
    return returnedPath

def Terminal_State(path):
    """
    Returns a end state's name from the path

    Parameters
    ----------
    path :  Path
        represents the path
    """   
    
    return path.nodes[0].name

def Expand(problem,path):
    """
    Returns a list of children nodes from the path's last node

    Parameters
    ----------
    problem : Graph.Graph
        The graph to search from S to G.
    path :  Path
        represents the path
    """  
    newPaths=[]
    curNode=path.nodes[0] # Current Node - The node to expand
    for child in curNode.edges:
        childExistsInPath=False
        #Need to check if child isn't there in the path
        for node in path.nodes:
            if node.name==child:
                childExistsInPath=True
        if (not childExistsInPath): # If the child doesn't exists in the path, add it
            parentPath=Path() # Setting a parent node
            for node in path.nodes:
                parentPath.nodes.append(node)
            parentPath.fn=path.fn   
            childNode = problem.getState(child) # Get the corresponding node with the name
            parentPath.addNode(childNode)
            newPaths.append(parentPath)
    return newPaths

def printQueue(queue, informedSearch):
    if(not informedSearch):
        print("[",end='')
        for path in queue:
            print("<",end='')
            countNode=0
            for node in path.nodes:
                print(node.name,end='')
                countNode+=1
                if(countNode<len(path.nodes)):
                    print(",",end='')
            print("> ",end='')
        print("]")
    else:
        print("[",end='')
        for path in queue:
            print(str(path.fn)+"<",end='')
            countNode=0
            for node in path.nodes:
                print(node.name,end='')
                countNode+=1
                if(countNode<len(path.nodes)):
                    print(",",end='')
            print("> ",end='')
        print("]")

def gn(path): 
    """
    Calculates the cost value of the path and returns it
    """
    cost=0.0
    for i in range(len(path.nodes)-1):
        cost+=path.nodes[i].edges[path.nodes[i+1].name]
    return cost

def hn(path):
    """
    Calculates the heuristic value of the path and returns it
    """
    return path.nodes[0].heuristic



def main(filename):
    """
    Entry point for this program. Parses the input and then runs each search on the parsed graph.

    Parameters
    ----------
    filename : str
        The name of the file with graph input to search
    """ 

    graph = readInput(filename)
    for search in SearchEnum:
        print(search.value)
        if (not General_Search(graph, search)):
            print("failure to find path between S and G")
        else:
            print("\tgoal reached!")
            # Print solution path here
        print()
def readInput(filename):
    """
    Build the graph from the given input file.

    Parameters
    ----------
    filename : str
        The name of the file with input to parse into a graph.
    """

    parsedGraph = Graph.Graph()
    isHeuristicSection = False # True if processing the heuristic values for the graph. False otherwise.
    sectionDivider = "#####"
    minCharsInLine = 3 # Each line with data must have at least 3 characters
    with open(filename, 'r') as input:
        for line in input.readlines():
            if (len(line) > minCharsInLine):
                line = line.strip()
                if(sectionDivider in line):
                    isHeuristicSection = True
                elif(isHeuristicSection):
                    state, heurStr = line.split(' ')
                    heuristic = float(heurStr)
                    parsedGraph.setHeuristic(state, heuristic)
                else:
                    state1, state2, costStr = line.split(' ')
                    cost = float(costStr)
                    parsedGraph.addStatesAndEdge(state1,state2, cost)
    for state_key in parsedGraph.states:
        state = parsedGraph.states[state_key]
        state.edges = OrderedDict(sorted(state.edges.items()))
    return parsedGraph   
if __name__ == "__main__": 
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Must input the filename with the graph input to search.")