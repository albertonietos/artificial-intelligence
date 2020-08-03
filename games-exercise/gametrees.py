# Both the Minimax and the Alpha-beta algorithm represent the players
# as integers 0 and 1. The moves by the two players alternate 0, 1, 0, 1, ...,
# so in the recursive calls you can compute the next player as the subtraction
# 1-player.
# The minimizing player is always 0 and the maximizing 1.

import math

from utils import count_calls

# Note, the decorator @count_calls is only used to count the number of calls.
# not needed for solving the exercise.
@count_calls
def minimax(player,state,depth_left):
    """
    Perform recursive min-max search of a game tree rooted in `state`.

    Returns the best value in the min-max sense starting from `state` for `player`
    using at most `depth_left`  recursive calls.

    Gives value of state if depth_left = 0 or the state has no further actions
    (a leaf in the game-tree).

    Parameters
    ----------
    player : int in {0,1}
       0 is the minimizing player, and 1 maximizing.
    state : GameState object.
       See `gamestate.py`.
    depth_left : int >= 0
       Maximum number of recursive levels to perform, including this this call to
       minimax.

    Returns
    -------
    float
       Best value.

    """
    if depth_left == 0 or len(state.applicable_actions(player)) == 0:
        return state.value()
    # TASK 1.1 Implement the minimax procedure.
    ### INSERT YOUR IMPLEMENTATION OF MINIMAX HERE
    ### It should be recursively calling 'minimax'.

    # The other player
    player_2 = 1 - player

    if player == 0:
        # player is minimizing
        best = float("inf")
    else:
        # player is maximizing
        best = -1 * float("inf")

    for action in state.applicable_actions(player):
        state_2 = state.successor(player, action)
        v = minimax(player_2, state_2, depth_left - 1)
        if player == 0:
            # minimizing
            best = min(best, v)
        else:
            # maximizing
            best = max(best, v)

    return best


# Note, the decorator @count_calls is only used to count the number of calls.
# not needed for solving the exercise.
@count_calls
def alphabeta(player,state,depth_left,alpha,beta):
    """
    Perform recursive alpha/beta search of game tree rooted in `state`.

    Returns the best value in the alpha/beta sense starting from `state` for `player`
    using at most `depth_left`  recursive calls.

    Gives value of state if depth_left = 0 or the state has no further actions
    (a leaf in the game-tree).

    Parameters
    ----------
    player : int in {0,1}
       0 is the minimizing player, and 1 maximizing.
    state : GameState object.
       See `gamestate.py`.
    depth_left : int >= 0
       Maximum number of recursive levels to perform, including this call to
       alphabeta.
    alpha : float
       Current alpha cut value.
    beta : float
       Current beta cut value.

    Returns
    -------
    float
       Best value.

    """
    if depth_left == 0 or len(state.applicable_actions(player)) == 0:
        return state.value()
    # TASK 1.2: Implement the alpha-beta procedure.
    ### INSERT YOUR IMPLEMENTATION OF ALPHABETA HERE
    ### It should be recursively calling 'alphabeta'.
    player_2 = 1 - player

    if player == 0:
        best = float("inf")
    else:
        best = -1 * float("inf")

    for action in state.applicable_actions(player):
        state_2 = state.successor(player, action)
        v = alphabeta(player_2, state_2, depth_left - 1, alpha, beta)

        if player == 0:
            best = min(best, v)
            beta = min(beta, v)
        else:
            best = max(best, v)
            alpha = max(alpha, v)

        if alpha >= beta:
            break

    return best


if __name__ == "__main__":
    from tictactoestate import *
    from pursuitstate import *

    def gamevalue(startingstate,depth):
        """ Helper function running minimax and alphabeta."""
        minimax.calls = 0
        v = minimax(0,startingstate,depth)
        print(str(v) + " value minimax to depth " + str(depth) + f" ; Calls: {minimax.calls}")
        alphabeta.calls = 0
        v = alphabeta(0,startingstate,depth,0-math.inf,math.inf)
        print(str(v) + " value with alphabeta to depth " + str(depth)+ f" ; Calls: {alphabeta.calls}")


    ttt = TicTacToeState()

    print(str(ttt))
    gamevalue(ttt,12)
    print("CORRECT VALUE for TicTacToe: 0 (Optimally played Tic Tac Toe -> draw)")

    testgrid1 = PursuitState(6,4,[[ 0, 0, 0, 0, 0, 0, 0],
                                  [ 0,-1, 0,-1, 0,-1, 0],
                                  [ 0,-1, 0,-1, 0,-1, 0],
                                  [ 1,-1, 1,-1, 1,-1, 1],
                                  [ 1,-1, 1,-1, 1,-1, 1]],
                             0,0,6,0,0)

    print(str(testgrid1))
    gamevalue(testgrid1,18)

    print("CORRECT VALUE for testgrid1: -993 (Crook is always captured)")



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

    print(str(testgrid2))
    gamevalue(testgrid2,16)

    print("CORRECT VALUE for testgrid2: -3998 (Crook is always captured)")

    print(str(testgrid3))
    gamevalue(testgrid3,18)

    print("CORRECT VALUE for testgrid3: 0 (Crook can run around the obstacle indefinitely)")

    print(str(testgrid4))
    gamevalue(testgrid4,16)

    print("CORRECT VALUE for testgrid4: -3998 (Crook is always captured)")
