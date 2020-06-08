Problem Solving with State-Space Search: Knights on the Chess board
-------------------------------------------------------------------

Human beings are good at problem solving: we are clever at coming up
new ways of thinking a problem, and finding features and regularities
in problems, making them easier to solve.

Existing A.I. is different: there are no computer programs that have the kind
of creative way of thinking as humans do. Instead, when solving hard problems
with computers, one usually substitutes clever thinking with the brute
force of the computer, the ability to go through thousands of different
alternatives in seconds.

The goal of the exercise is to implement data structures for representing
different game board configuration with only Chess Knights on them,
and then trying to solve puzzles that involve moving the pieces
from one configuration to another according to the legal moves.

The sample problems are solved with a basic Breadth-First Search algorithm,
which is given in the code (in the next exercise we will be looking at algorithms that
are usually far better than BFS).

Your task is to implement a `successor` function of a class representing a game-board state.
This function has the task of producing all possible movement of the Knights on the Chess board.

You are not required to write the program from scratch: we
provide a skeleton of the program where some sections of the code have
to be just filled in.

- Copy `template-knightsstate.py` to `knightsstate.py`.
  
- Read through the given code, and try to understand its functioning.

- Look for the comment `TASK` in the file `knightsstate.py`, your implementation should go there.
  
- We have also provided a basic outline of the algorithm in the comments for this first exercise.

Please **only modify the indicated parts of the code**
to keep it compatible with the automated testbench for evaluating the program.

*Testing:* You can test your implementation with the test cases included in the code: :code:`python test_knightsstate.py`.

*Examples:* The implementation of the Breadth First Search algorithm in `bfs.py` contains some example puzzles using Knight states. Once you have implemented the task you can run: :code: `python bfs.py` to search for policies for getting from one board configuration to another.

