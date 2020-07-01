Programming exercise: Encoding logic formulas using the z3 module
-----------------------------------------------------------------

For the exercises in the logic round we will be using an SMT - Satisfiability
Modulo Theories - solver called z3. It has been developed by Microsoft and is
freely available with binding for several programming languages.

In this first exercise you will practice encoding three different Boolean
formulas using the z3 Python classes  `And,Or,Not,Implies`.

(Note: SMT solvers are not restricted to Boolean formulas, but in this round we
will only work with these.)

Instructions
^^^^^^^^^^^^
1. If you have not done so already, download and set up the z3 SMT solver for
   Python. If you are using python pip package manager this can be done with
   `pip install z3-solver.` You can also install it with conda and other scientific
   python managers. See https://github.com/Z3Prover/z3 for more information.
2. Read and understand all code.
3. Copy the file `template-z3warmup.py` to `z3warmup.py`

Tasks
^^^^^
1. Look at the implementation of the function `example_1`, which shows how to encode the formula (a ⇒ b) ∧ (¬b ∨ c).
2. Implement the function `task_1`, returning the formula (a ⇒ ¬b) ∨ (b ⇒ a ∧ c) ∨ d .
3. Implement the function `task_2`, returning the formula (a ⇒ (b ⇒ (c ⇒ (d ⇒ e)))) ∧ f .
4. Implement the function `task_3`, returning the formula a ⇒ b ∧ ¬c ∨ ¬b ∧ c .

Testing
^^^^^^^
- `python z3warmup.py` : will print the mathematical expression of the implemented formulas so that you can check what you have implemented. (No unit test is provided for this basic exercise.)

Note: If your terminal can not properly display the Unicode characters for the formulas you can also submit z3warmup.py for grading - if your formula is not an equivalent model the error will show both the submitted formula and the expected one.
 
