
from queue import Queue

def bfs(start_state, goaltest):
    """
    Find a sequence of moves through a state space by breadth first search.
    
    This function returns a policy, i.e. a sequence of actions which, if 
    applied to `start_state` in order, will transform it to a state which 
    satisfies `goaltest`.

    Parameters
    ----------
    start_state : State
       State object with `successors` function.
    goaltest : Function (State -> bool)
       A function which takes a State object as parameter and returns true if 
       the state is an acceptable goal state.
    
    Returns
    -------
    list of actions
       The policy for transforming start_state into one which is accepted by
       `goaltest`.
    """
    # Is the start_state also a goal state? Then just return!
    if goaltest(start_state):
        return []
    
    # Otherwise...
    # Need to keep track of visited states to make sure that there are no loops.
    # The start_state is already checked above, so add that.
    visited = {start_state}
    # And we also need a dictionary to look up predecessor states and the
    # the actions which took us there. It is empty to start with.
    predecessor = {}
    # Use a queue to track the states which should be expanded.
    Q = Queue()
    # Initially there's only the start state.
    Q.put(start_state)

    # Begin search.
    while not Q.empty():
        # Get next state to be expanded.
        state = Q.get()
        # Check all its successor states.
        for (action,ss) in state.successors():
            # Only work with states not already visited.
            if ss not in visited:
                # Update predecessor.
                predecessor[ss] = (state,action)
                # Check goal.
                if goaltest(ss):
                    # This is the state we are looking for!
                    # Create a of actions path by stepping back through
                    # the predecessors.
                    (last_state, last_action) = predecessor[ss]
                    pi = [last_action]
                    # As long as the predecessor state is not the initial state
                    while last_state != start_state:
                        # Update the policy.
                        (last_state, last_action) = predecessor[last_state]
                        pi.append(last_action)
                    # Return the policy, reversed (because we constructed it
                    # from end to start state).
                    return reversed(pi)
                # Not a goal state, need to keep searching.
                # Mark state as visited.
                visited.add(ss)
                # Enqueue successor.
                Q.put(ss)
    # If the queue becomes empty without the goal test triggering a return
    # there is no policy, so return None.
    return None
            
if __name__ == "__main__":
    from knightsstate import KnightsState

    # Example 1
    #
    # KK......  ........
    # KK......  ........
    # ........  ..KK....
    # ........  ..KK....
    # ........  ........
    # ........  ........
    # ........  ........
    # ........  ........
    print("Move four knights in a 2 by 2 formation 2 steps diagonally.")
    print("This will take about a second to solve.")
    ks1 = KnightsState([(0,0),(0,1),(1,0),(1,1)])
    ks2 = KnightsState([(2,2),(2,3),(3,2),(3,3)])
    print("Start state:")
    print(ks1)
    print("Target state:")
    print(ks2)
    pi = bfs(ks1, lambda s : s == ks2)
    print(f"Policy: {', '.join(str(a) for a in pi)}")
    print("---------------------------------------------------")

    # Example 2
    # KKK.....  ........
    # KK......  ........
    # ........  ..KKK...
    # ........  ..KK....
    # ........  ........
    # ........  ........
    # ........  ........
    # ........  ........
    print("Move five knights in a 3+2 formation 2 steps diagonally.")
    print("This will take about 20 seconds to solve.")
    ks1 = KnightsState([(0,0),(0,1),(0,2),(1,0),(1,1)])
    ks2 = KnightsState([(2,2),(2,3),(2,4),(3,2),(3,3)])
    print("Start state:")
    print(ks1)
    print("Target state:")
    print(ks2)
    pi = bfs(ks1, lambda s : s == ks2)
    print(f"Policy: {', '.join(str(a) for a in pi)}")
    print("---------------------------------------------------")

    # Example 3
    #
    # KKK.....  ........
    # KKK.....  ........
    # ........  ..KKK...
    # ........  ..KKK...
    # ........  ........
    # ........  ........
    # ........  ........
    # ........  ........
    print("Move six knights in a 3+3 formation 2 steps diagonally.")
    print("This will take about one minute to solve.")
    ks1 = KnightsState([(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)])
    ks2 = KnightsState([(2,2),(2,3),(2,4),(3,2),(3,3),(3,4)])
    print("Start state:")
    print(ks1)
    print("Target state:")
    print(ks2)
    pi = bfs(ks1, lambda s : s == ks2)
    print(f"Policy: {', '.join(str(a) for a in pi)}")
    print("---------------------------------------------------")
    
