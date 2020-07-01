Programming exercise: Sudoku Solver
-----------------------------------

In this exercise you will implement parts of a constraint-based solver for
Sudoku puzzles.

Instructions
^^^^^^^^^^^^
1. If you have not done so already, download and set up the z3 SMT solver for
   Python. If you are using python pip package manager this can be done with
   `pip install z3-solver.` You can also install it with conda and other scientific
   python managers. See https://github.com/Z3Prover/z3 for more information.
2. Read and understand all code.
3. Copy the file `template-sudoku.py` to `sudoku.py`
4. Review the logic lecture (Lecture number 4).

Tasks
^^^^^
There are five sub-tasks in this exercise, all marked with the comment TASK in
the file `sudoku.py`:

1. Implement the function `atMost1`.
2. Implement the function `exactly1`.
3. Implement constraints C2 - every row has all numbers.
4. Implement constraints C3 - every column has all numbers.
5. Implement constraints C4 - every sub-grid has all numbers.

The definition of these functions and constraints can be found in the logic
lecture material.

Testing
^^^^^^^

1. `python test_sudoku.py` : Will run some basic unit tests. Note that if one
   more more of these fails for the sudoku puzzles it might be useful run the next
   item too.
2. `python sudoku.py` : Will attempt to solve three example Sudoku puzzles and
   will also pretty-print the clues as well as the solutions (all are solvable).
   Doing a visual inspection of the print-outs might give you a good idea of any
   problem with your constraints (such as if there are numbers missing, or if a
   number occurs twice in a row for instance.

Discussion
^^^^^^^^^^
Have a look at the visualization of the brute-force backtracking article in the
Wikipedia article (https://en.wikipedia.org/wiki/Sudoku_solving_algorithms). For
easy Sudoku puzzles the solution we are using often beats blind backtracking hands
down, and for hard Sudoku a blind backtracking search (without inferences) is even
worse. 


Good luck!
