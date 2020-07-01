"""
Warm up exercise with z3.
"""
# This exercise uses Microsoft's Z3 SMT solver (https://github.com/Z3Prover/z3).
# You can install it for python using e.g. pip: `pip install z3-solver`
# or see the github page for more option.s
#
# z3 is an SMT - Satisfiability Modulo Theories - solver, and isn't restricted
# to working with Booleans, but for the purpose of instruction we will only
# use the Bool sort in this round.

# These are the operators we will be using.
from z3 import And,Or,Not,Implies
# Bool/Bools are used to create Boolean atoms.
from z3 import Bool, Bools
# This is used to solve and check satisfiability of a set of formulas.
from z3 import Solver,sat
# Below used for pretty printing only.
from z3 import z3printer
# The html module is only used for pretty printing.
import html

def example_1(a,b,c):
    """
    Encodes the formula (a ⇒ b) ∧ (¬b ∨ c)

    Parameters
    ----------
    a,b,c : Bool
       Variables of the formula.

    Returns
    -------
    z3 formula
    """
    # And / Or can either be called with a list of other formulas/variables or
    # with a set of arguments.
    # Here we show both; 'And' is given a list: `And([ ... ])`, while 'Or' is
    # called with arguments directly: `Or(Not(b),c)`.
    # 'Implies' takes two arguments (formulas or variables).
    # 'Not', of course takes one formula/variable and negates it.
    # Make sure you see how the below encode (a ⇒ b) ∧ (¬b ∨ c)
    return And([Implies(a,b), Or(Not(b),c)])

def task_1(a,b,c,d):
    """
    Encodes the formula (a ⇒ ¬b) ∨ (b ⇒ a ∧ c) ∨ d

    Parameters
    ----------
    a,b,c,d : Bool
       Variables of the formula.

    Returns
    -------
    z3 formula
    """
    # TASK 1: Return the formula in the function docstring.
    # Note: Precedence among the logic operators: ¬,∧,∨,⇒ (from left to right)
    #       E.g. b ⇒ a ∧ c is the same as b ⇒ (a ∧ c).
    return # Encode formula here.

def task_2(a,b,c,d,e,f):
    """
    Encodes the formula (a ⇒ (b ⇒ (c ⇒ (d ⇒ e)))) ∧ f

    Parameters
    ----------
    a,b,c,d,e,f : Bool
       Variables of the formula.

    Returns
    -------
    z3 formula
    """
    # TASK 3: Return the formula in the function docstring.
    return # Encode formula here.

def task_3(a,b,c):
    """
    Encodes the formula a ⇒ b ∧ ¬c ∨ ¬b ∧ c

    Parameters
    ----------
    a,b,c,d,e,f : Bool
       Variables of the formula.

    Returns
    -------
    z3 formula
    """
    # TASK 3: Return the formula in the function docstring.
    # Note: Precedence among the logic operators: ¬,∧,∨,⇒ (from left to right)
    #       Tip: Use this to put parenthesis in the formula if you are having
    #            trouble encoding it.
    return # Encode formula here.

def uc(fma):
    """
    Get a mathematical expression of formula using Unicode symbols.

    Utility function.

    Parameters
    ----------
    fma : z3 formula
       The formula.

    Returns
    -------
    str
       Mathematical representation of formula as unicode string.
    """
    z3printer.set_html_mode(True)
    return html.unescape(z3printer.obj_to_string(fma))
    
if __name__ == "__main__":
    # Declare some boolean variables.
    # These need a name as parameter, and can either be declared one by one as
    a = Bool('a')
    b = Bool('b')
    # Or, they can be declare in bulk using Bools:
    c,d,e,f = Bools('c d e f')
    
    f1 = example_1(a,b,c)
    print(f"Example 1: {uc(f1)}")

    t1 = task_1(a,b,c,d)
    print(f"Task 1: {uc(t1)}")

    t2 = task_2(a,b,c,d,e,f)
    print(f"Task 2: {uc(t2)}")

    t3 = task_3(a,b,c)
    print(f"Task 3: {uc(t3)}")

    # Solving:
    # As an example of how to solve a system:
    # One can find a model for formulas by creating a solver and adding
    # all formulas which needs to be satisfied.
    # E.g. to see if the conjunction of all the declared formulas has a
    # satisfying assignment we can do:
    s = Solver()
    s.add(f1) # Add the formula f1
    s.add(t1) # And t1
    s.add(t2) # And t2
    s.add(t3) # And t3
    if s.check() == sat: # Check if a solution exists.
        # Is the system of all these satisfiable by some model?
        print("The conjunction of f1,t1,t2,t3 is satisfiable.")
        # This is how you get A model (there might be more)
        m = s.model()
        # The model can be queried for the values of its components,
        # here we'll just print it.
        print(f"A possible assignment is: {m}")
    else:
        # Not satisfiable.
        print("The conjunction of f1,t1,t2,t3 is not satisfiable.")
