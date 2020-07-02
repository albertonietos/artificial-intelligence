Programming Exercise 2: the Zebra Puzzle
-----------------------------------------

The Zebra Puzzle (https://en.wikipedia.org/wiki/Zebra_Puzzle) is an old - and today, perhaps a bit aged - logic puzzle.

As you've heard about in the lecture, it consists of a dozen or so statements about five gentlemen living in five different coloured houses, each with a different pet, drinking different beverages, and smoking different mid twentieth century US tobacco brands.

The question is: who keeps a zebra (hence the name) and who drinks water?

In this exercise we'll implement the zebra puzzle as predicates and solve it using the z3 SMT module in Python. Your tasks concerns encoding a number of the constraints necessary to obtain a correct solution.

Instructions
^^^^^^^^^^^^
1. Copy the file `template-zebrapuzzle.py` to `zebrapuzzle.py`
2. Read and understand the code.
   - The code first sets up the 'sorts', i.e. types of the puzzle universe (drinks, animals, ...)
   - Then a number of functions are created, e.g. a function 'Drinks' describing who drinks what.
   - Then the constraints of the puzzle are written as z3 predicates using quantifiers (Exists, ForAll) when necessary.
   - Several of the puzzle constraints are already implemented, so it is worth taking the time understanding these before tacking the tasks.
3. There are nine predicates to implement, named TASK 1 ... TASK 9.
4. In each case, you should replace the `True` value with an expression for the predicate.
5. Only change the code for the TASKs; don't define any functions of your own.
6. Some constraints will require you to use quantifier expressions (Exists, ForAll).

*Tip:*

- You can run `python zebrapuzzle.py` to have z3 provide a model for the puzzle with the current constraints (even without implementing any of the tasks). Naturally this model is not a solution to the puzzle. This is possible because the constraints for the TASKs are initially set to `True` (try to set one of them to `False` and see what happens. Why is this?).
- Using this, it might make sense to implement one constraint at the time, solve it, and check in the output if it worked as intended.

Testing
^^^^^^^
1. `python test_zebrapuzzle.py` : Will run a set of unit tests. These are *not* exhaustive (not to give the exercise away); the tests only checks for quantifier expressions when expected, and uses counter-examples to try to catch missing constraints.
2. `python zebrapuzzle.py` : As mentioned above, this will attempt to find a model for the puzzle (will take a few seconds - some minute when all constraints are in place). If a correct solution is printed and your tests are passing, you probably have a good implementation.


Good luck!






