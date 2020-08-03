Implementing Minimax and Alpha-Beta Pruning
-------------------------------------------

The goal of the exercise is to implement the Minimax algorithm, add alpha-beta
pruning to it, and experiment with the implementation to determine the
effectiveness of pruning.

The overall specification for the functions is as follows:

1. The input is a game tree represented implicitly
   by the initial state of the game, the set of actions,
   and functions for determining the successor state of a state
   with respect to a given action.

2. The output is the highest possible reward the maximizing
   player can achieve for the game given as input.

The Minimax implementation is generic, and can be used in connection with *any*
game represented as a subclass of the class `GameState` (see `gamestate.py`). As
test material we provide implementations of Tic Tac Toe (`tictactoestate.py`) as
well as a simple pursuit-evasion game (`pursuitstate.py`), in which the Police
chases a Crook in a 2-dimensional grid. The thief is trying to collect rewards
from the grid cells, and the police is trying to catch the crook (by entering
the same cell) to incur a large negative reward to the crook.

You are not required to write the program from scratch, since we provide a
skeleton of the program where some sections of the code have to be just filled
in. Please **do not modify** the given parts of the code in order to keep your
approach compatible with the test bench used to evaluate your program.

Instructions
^^^^^^^^^^^^
1. Read about the minimax algorithm and alpha-beta pruning
2. Copy `template-gametrees.py` to `gametrees.py`
3. Read and understand all the code
4. Implement the tasks

Tasks
^^^^^
- TASK 1.1: Implement function `minimax` (game-tree search using the minimax
  procedure)
- TASK 1.2: Implement function `alphabeta` (game-tree search using the alpha-beta
  procedure)
  
Testing
^^^^^^^
- `python gamestrees.py` :: Will run a few examples, print the number of calls
  and the correct answers. (Note the difference in the number of calls betwen
  minimax and alphabeta.)
- `python test_qlearn.py` :: Will execute very basic unit tests.


Notes
^^^^^
- The examples in gametrees.py may take some time (minutes, depending on
  computer) to execute
- Due to complexity the unit tests are quite basic, it is recommended to check
  that both unit tests and examples run fine
- `minimax` and `alphabeta` are recursive functions.
- Functions `minimax` and `alphabeta` are decorated with `@count_calls`; this is
  simply to be able to count the number of function calls (see `utils.py` if you
  are interested), and there is no need to use it for the exercise tasks.


