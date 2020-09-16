from enum import Enum, auto
class SearchEnum(Enum):
    """
    A class used to represent the searches to implement and the title to use when outputting their respective results.
    """
    
    DEPTH_FIRST_SEARCH = "Depth 1st search"
    BREADTH_FIRST_SEARCH = "Breadth 1st search"
    DEPTH_LIMITED_SEARCH = "Depth-limited search (depth-limit = 2)"
    ITERATIVE_DEEPENING_SEARCH = "Iterative deepening search"
    UNIFORM_COST_SEARCH = "Uniform Search (Branch-and-bound)"
    GREEDY_SEARCH = "Greedy Search"
    A_STAR = "A*"
    HILL_CLIMBING = "Hill climbing without backtracking"
    BEAM_SEARCH = "Beam search (w = 2)"
