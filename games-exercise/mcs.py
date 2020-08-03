import random
from math import inf

# Evaluate a state
# Monte Carlo search: randomly choose actions
def mc_trial(player,state,steps_left):
    """
    Recursively perform Mote Carlo Trial randomly choosing among available
    actions for next state.

    Performs at most steps_left moves, if steps_left = 0 or if there are no
    applicable actions for `player` in `state`, it will return the state value.

    Parameters
    ----------
    player : int in [0,1]
       Current player.
    state : GameState object.
       See `gamestate.py`.
    steps_left : int >= 0
       Maximum number of recursive levels to perform.

    Returns
    -------
    float
       Value of final state.
    """
# TASK 2.1: Implement mc_trial such that your code chooses one action uniformly
# at random, executes it to obtain a successor state, and continues simulation
# recursively from that successor state, until there are no steps left. Then the
# value of the state is returned.
# CODE HERE




def mc_search(player,state,trials,trial_depth):
    """
    Repeatedly perform Monte Carlo Trials and return the average value.

    Parameters
    ----------
    player : int in {0,1}
       Current player.
    state : GameState object.
       See `gamestate.py`.
    trials : int > 0
       Number of Monte Carlo Trials to perform.
    trial_depth : int > 0
       Maximum number of recursive depth per for each trial.

    Returns
    -------
    float
       Average value of the trials.

    """
# TASK 2.2: Execute mc_trial `trial` number of times, and return the average of
# the results.
# CODE HERE



# ------------------------------------------------------------------------------
### TOP-LEVEL PROCEDURE FOR USING MONTE CARLO SEARCH
### The game is played by each player alternating
### with a choice of their best possible action,
### which is chosen by evaluating all possible
### actions in terms of the value of the random
### walk in the state space a.k.a. Monte Carlo Search.

def mc_execute(player,state,moves_left,trials):
    """
    Recursively play a game using Monte Carlo Search printing successive states.

    Function alternates between players.

    Parameters
    ----------
    player : int in {0,1}
       Current player.
    state : Object representing game state.
       See `gameexamples.py` for examples.
    moves_left : int >= 0
       Number of moves to simulate.
    trials : int > 0
       Number of Monte Carlo Trials in each sample.

    """
    if moves_left>0:
        if player==0:
            bestScore = inf # Default score for minimizing player
        else:
            bestScore = -inf # Default score for maximizing player
        actions = state.applicable_actions(player)
        if len(actions)>0:
            for action in actions:
                state0 = state.successor(player,action)
                v = mc_search(1-player,state0,trials, moves_left)
                if player==1 and v > bestScore: # Maximizing player chooses highest score
                    bestAction = action
                    bestScore = v
                if player==0 and v < bestScore: # Minimizing player chooses lowest score
                    bestAction = action
                    bestScore = v
            state2 = state.successor(player,bestAction)
            return mc_execute(1-player,state2,moves_left-1,trials)
    return state.value()

if __name__ == "__main__":

    from tictactoestate import *
    from pursuitstate import *
    ttt = TicTacToeState();
    # Next tests play the games by choosing the next actions according
    # to the most promising action found by Monte Carlo Search.
    # Comments:
    # If both players play optimally, Tic Tac Toe ends in a draw. A basic tree
    # search trivially finds the optimal moves for both players, but MCS even
    # with thousands of simulations does not always yield the best moves, and
    # the above simulation often ends up one player winning.
    # The pursuit-escape game is played better by MCS. Only in testgrid3 can
    # the crook evade capture by the police. MCS often chooses the best
    # moves for the police, but not always.


    # No score printed due to the nondeterministic nature.
    print("###################### PLAY TIC TAC TOE ######################")
    v = mc_execute(0,ttt,12,5000)
    if v == 0:
        print("Draw")
    elif v < 0:
        print("Player 0 wins.")
    else:
        print("Player 1 wins.")
    testgrid1 = PursuitState(6,4,[[ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0,-1, 0,-1, 0,-1, 0],
                                  [ 0,-1, 0,-1, 0,-1, 0],
                                  [ 1,-1, 1,-1, 1,-1, 1],
                                  [ 1,-1, 1,-1, 1,-1, 1]],
                             0,0,6,0,0);

    testgrid2 = PursuitState(3,3,[[ 0, 0, 0, 0],
                                  [ 0, 0, 0, 0],
                                  [ 0, 0, 0, 0],
                                  [ 1, 0, 0, 0]],
                             0,0,3,0,0);

    testgrid3 = PursuitState(3,3,[[ 0, 0, 0, 0],
                                  [ 0, 0, 0, 0],
                                  [ 0, 0,-1, 0],
                                  [ 1, 0, 0, 0]],
                             0,0,3,0,0);

    testgrid4 = PursuitState(3,3,[[ 0, 0, 0, 0],
                                  [ 0,-1, 0, 0],
                                  [ 0, 0, 0, 0],
                                  [ 1, 0, 0, 0]],
                             0,0,3,0,0);


    print("###################### CHASE IN TEST GRID 1 ######################")
    v = mc_execute(0,testgrid1,20,2000)
    if v < 0:
        print("The robber got caught (at least once).")
    else:
        print("The robber can avoid the police.")

    print("###################### CHASE IN TEST GRID 2 ######################")
    v = mc_execute(0,testgrid2,30,3000)
    if v < 0:
        print("The robber got caught (at least once).")
    else:
        print("The robber can avoid the police.")
    print("###################### CHASE IN TEST GRID 3 ######################")
    v = mc_execute(0,testgrid3,30,2000)
    if v < 0:
        print("The robber got caught (at least once).")
    else:
        print("The robber can avoid the police.")

    print("###################### CHASE IN TEST GRID 4 ######################")
    v = mc_execute(0,testgrid4,30,2000)
    if v < 0:
        print("The robber got caught (at least once).")
    else:
        print("The robber can avoid the police.")
