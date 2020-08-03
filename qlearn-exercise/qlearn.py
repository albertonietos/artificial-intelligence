"""
Performs q-learning.
"""

import random
from utils import argmax


# Looks up the best value for a state in the Q table.
def value_best_action(state,Q):
    """
    Return value of best available action in `Q` given `state`.
    
    Parameters
    ----------
    state : pair of (int,int)
    Q : dict of dict{(int,int) : dict {GridAction : float}}
       Q dictionary mapping from state to action to float.

    Returns
    -------
    float
       Maximum Q-value for any action in `state`.
    
    """
    # TASK 1: return the value of the best possible action for `state`.
    # Hint: Note that the argmax function is imported from utils.
    ### YOUR CODE HERE
    ### YOUR CODE HERE
    ### YOUR CODE HERE
    score = 0.0
    for action in Q[state]:
        if Q[state][action] > score:
            score = Q[state][action]

    return score


# 'execute' randomly chooses a successor state for state s w.r.t. action a.
# The probability with which is given successor is chosen must respect
# the probability of the MDP.
# It returns a tuple (s2,r), where s2 is the successor state and r is
# the reward that was obtained.

def execute(mdp,s,a):
    """
    Randomly choose a successor state of state `s` given action `a`.

    The probability of the successor state respects the probability of the
    Markov Decision Process.
    
    Parameters
    ----------
    mdp : GridMDP object (see `gridmdp.py`)
    s : (int,int)
       Current state as pair of int.
    a : int
       Action as int in GridMDP.ACTIONS (`[1,2,3,4]` in effect)
    
    Returns
    -------
    ((int,int),float)
       Chosen successor state and associated reward.
    """
    # TASK 2: Implement `execute` to randomly pick one of the possible
    # successor states and return it.
    # Note that you can not pick the states uniformly.
    # Tip: You have access to python's random module. This may contain useful
    # functions. See https://docs.python.org/3.7/library/random.html
    ### YOUR CODE HERE
    ### YOUR CODE HERE
    ### YOUR CODE HERE
    ss = mdp.successor_states(s, a)
    state = [s[0] for s in ss]
    prob = [s[1] for s in ss]
    reward = [s[2] for s in ss]

    choice = random.choices(state, prob)[0]
    # print(reward, choice, state.index(choice[0]))
    rchoice = reward[state.index(choice)]

    return (choice, rchoice)




# q_learning returns the Q-value table after performing the given
#   number of iterations i.e. Q-value updates.
def q_learning(mdp,gamma,lambd,iterations, start_state = (0,0)):
    """
    Perform the Q-learning algorithm on Markov Decision Process."

    Initializes a Q table to 0 for all states and actions and starting from 
    `start_state` performs `iterations` number of updates.

    Parameters
    ----------
    mdp : GridMDP object (see `gridmdp.py`)
       Markov Decision Process
    gamma : float in [0,1]
       Discount factor.
    lambd : float in [0,1]
       Learning rate.
    iterations : int > 0
       Number of iterations to perform.
    start_state: (int, int)
       Initial state for algorithm.

    Returns
    -------
    Q : dict of dict{(int,int) : dict {GridAction : float}}
       Q dictionary mapping from state to action to float.
    """

    # The Q-values are a real-valued dictionary Q[s][a] where s is a state and a is an action.
    # Initialize it to 0.
    Q = {s: {a : 0 for a in mdp.applicable_actions(s)} for s in mdp.states()}  
    s = start_state
    # Let s be the current state, and make sure it is set to start_state.
    # TASK 3: Implement the q_learning algorithm, returning the final Q dictionary.
    # See The course material, section 8.2 for an algorithm.
    # Note:
    #      1. 'Some action' means pick an action uniformly at random.
    #      2. `execute` in Task 2 should be used to pick the next state,reward
    #      2. The algorithm should run for `iterations` number of iterations.
    ### YOUR CODE HERE
    ### YOUR CODE HERE
    ### YOUR CODE HERE
    return Q




# make_policy constructs a policy, i.e. a mapping from state to actions,
#   given a Q-value function as produced by q_learning.
def make_policy(mdp,Q):
    """
    Get policy for states in `mdp` given Q-values `Q`.

    Parameters
    ----------
    mdp : GridMDP object (see `gridmdp.py`)
       Markov Decision Process
    Q : dict {(action,state) : float}
       As returned by function `q_learning`.

    Returns
    -------
    dict {(int,int) : GridAction}
       Dictionary to look up the optimal action given a state.
    """
    # A policy is an action-valued dictionary P[s] where s is a state
    pi = dict()
    # TASK 4: Fill in P with the best action for every state in `mdp`.
    ### YOUR CODE HERE
    ### YOUR CODE HERE
    ### YOUR CODE HERE
    return pi




# make_values constructs the value function, i.e. a mapping from states to values,
#   given a Q-value function as produced by q_learning.
def make_values(mdp,Q):
    """
    Get best values for states in `mdp` given Q-values `Q`.
    
    Parameters
    ----------
    mdp : GridMDP object (see `gridmdp.py`)
       Markov Decision Process
    Q : dict of dict{(int,int) : dict {GridAction : float}}
       Q dictionary mapping from state to action to float.
    
    Returns
    -------
    dict {(int,int) : float}
       Values of best action for every state of `mdp`.
    """
    v = dict()
    v = {s : value_best_action(s,Q) for s in mdp.states()}
    return v

if __name__ == '__main__':
    from utils import *
    from gridmdp import *
    
    testgrid1 = GridMDP(["-*-#",
                         "...#",
                         "...#",
                         "####"],
                        tile_rewards = {'*':20, '-':-1},
                        no_move_reward = -1)
    
    
    print("Input GridMDP:")
    print(testgrid1)
    
    Q1 = q_learning(testgrid1,0.85,0.1,20000,
                    start_state = (2,1))
    pi = make_policy(testgrid1,Q1)
    v = make_values(testgrid1,Q1)
    print("----------")
    print("policy:")
    visualize_policy(testgrid1,pi)
    print("----------")
    print(f"Shortest distance from (2,1) to (0,1) is 2, your code gives {follow_pi(pi,(2,1),(0,1),testgrid1)}.")
    print(f"Shortest distance from (2,2) to (0,1) is 3, your code gives {follow_pi(pi,(2,2),(0,1),testgrid1)}.")
