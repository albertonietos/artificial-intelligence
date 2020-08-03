Implementing Monte Carlo Search
-------------------------------

The goal of this exercise is an implementation of Monte Carlo Search
for choosing the next action by a randomly simulating the game in all possible
next states for a large number of times. For every possible first action,
the average outcome of the subsequent simulations yields a score (e.g. average
of outcomes of all simulations), and the next action is determined by the scores.


The overall specification for the functions is as follows:

1. The input is a game tree represented implicitly
   by the initial state of the game, the set of actions,
   and functions for determining the successor state of a state
   with respect to a given action.

2. The output is the highest possible reward the maximizing
   player can achieve for the game given as input.

The implementation is generic, and can be used in connection with *any*
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
1. Read about Monte-Carlo search
2. Copy `template-mcs.py` to `mcs.py`
3. Read and understand all the code
4. Implement the tasks
   
Tasks
^^^^^
- TASK 2.1: Implement function `mc_trial` (this is heart of an MC search)
- TASK 2.2: Implement function `mc_search` (calculating the average from a
  number of MC trials)

Testing
^^^^^^^
- `python mcs.py` :: Will run a few examples and print the results.
- `python test_mcs.py` :: Will execute very basic unit tests.

Notes
^^^^^
- Pick the next action uniformly at random
- The tests may take a few moments (but not as long as those for the previous
  tasks) to run
- Monte-Carlo is a stochastic procedure:
  - For the examples, there is a chance that you might not get the expected
    result (for example a draw in tic-tac-toe)
  - If you are really, really unlucky the third unit test might indicate an
    error where there is none due to it being based on a statistic (this is
    not always good practice, but in this case it will also help to catch
    a common mistake when picking actions). If you are sure you have no error
    you can always run the test again... but if it keeps indicating an error
    there probably is one.
- `mc_trial` is a recursive function

