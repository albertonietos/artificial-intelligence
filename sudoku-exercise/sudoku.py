"""
Solve a Sudoku puzzle using logic constraints.
"""
# This exercise uses Microsoft's Z3 SMT solver (https://github.com/Z3Prover/z3).
# You can install it for python using e.g. pip: `pip install z3-solver`
# or see the github page for more option.s
#
# z3 is an SMT - Satisfiability Modulo Theories - solver, and isn't restricted
# to working with Booleans, but for the purpose of instruction we will only
# use the Bool sort in this round.

from z3 import And,Or,Not,Bool,Solver,sat

######### Cardinality constraints #########
def allpairs(lst):
    """
    Helper function, giving all pairs of a list of formulas.
    
    Parameter
    --------
    lst : list of formulas

    Returns
    -------
    generator of pairs
       Each unique pairing of the formulas in `lst`.
    """
    return ( (lst[i],lst[j]) for i in range(0,len(lst)) \
             for j in range(i+1,len(lst)) )

def atLeast1(fmas):
    """
    Expresses that at least one formula in a list must be true.

    Parameters
    ----------
    fmas : list of formulas (len > 1)
       Of this list, at least one expression must evaluate to true.

    Returns
    -------
    Formula
    """
    # At least one true is easy. Disjuction.
    return Or(fmas)


def atMost1(fmas):
    """
    Expresses that at most one formula in a list must be true.

    Parameters
    ----------
    fmas : list of formulas (len > 1) 
       Of this list, at least at most one must be true.

    Returns
    -------
    Formula
    """
    # TASK 1: Implement atMost1 - see lecture material for definition.
    # Hint: You can use the function 'allpairs' above to get the pairing
    #       of formulas.
    return And([Not(And(pair)) for pair in allpairs(fmas)]) # YOUR FORMULA HERE
def exactly1(fmas):
    """
    Expresses that exactly one formula in a list must be true.

    Parameters
    ----------
    fmas : list of formulas (expressed as And, Or, Not, or using a Bool Atom).
       Of this list, at least one expression must evaluate to true.

    Returns
    -------
    Formula
    """
    # TASK 2: Implement exactly1 - see lecture material for definition.
    return And(atLeast1(fmas), atMost1(fmas)) # YOUR FORMULA HERE

######### Translation of Sudoku to propositional logic #########

def S(c,r,n):
    """
    Creates an atom expressing that the cell at r,c contains number n.

    This is just a wrapper to create a Bool constant with a string
    representing the particular row, column, number.
    
    Note: In the lecture material the order of row and column are swapped,
    so that S(r,c,v) is denoted S_{c,r,v}.

    Parameters
    ----------
    r : int in [1,9]
       Row coordinate.
    c : int in [1,9]
       Column coordinate.
    n : int in [1,9]
       Integer.
    

    Returns
    -------
    z3.BoolRef
       Boolean valued atom to be used in formulas.
    """
    return Bool(f"{r}_{c}_{n}")

 

def sudoku2fma(puzzle):
    """
    Map 9X9 Sudoku instances to propositional formulas.

    Parameters
    ----------
    puzzle : dict of (row, column) : number
       The given Sudoku clues as the number for location (row, column).
        row, column, and number all in the range [1,9]
       A missing (row,column) key indicates that the number at that location
       is unknown.

    Returns
    -------
    tuple
       (C1,C2,C3,C4,C5) as Z3 formulas.
    """

    # Note: In the lecture material the order of row and column are swapped,
    # so that S(r,c,v) is denoted S_{c,r,v}.
    # Consequently the constraints C2 and C3 have changed order here.
    # This does not really matter due to symmetry - as long as one of them deals
    # with rows and the other with columns, but just in case you notice
    # and wonder about it while reading the code.

    # In formulas C2 to C4 below, instead of exactly1 it would be logically
    # equivalent to use Or - the lecture slides show both alternatives.
    # However, the exactly1 allows Unit Propagation in basic DPLL solvers
    # to infer far more new literals, and cutting down the size of the search tree
    # to a small fraction.
    # For z3 - the solver we use now, this should matter little in this case, 
    # but have a go at using exactly1 in any case.

    # Note: In the lecture material the order of row and column are swapped,
    # so that S(r,c,v) is denoted S_{c,r,v}.
    # This does not really matter due to symmetry - as long as one of them deals
    # with rows and the other with columns, but just in case you notice
    # and wonder about it while reading the code.

    # Constraints
    # -----------
  
    # Every grid cell has exactly one value, basically:
    # there is exactly one of numbers 1..9 in (1,1) and in (1,2) and in (1,3)
    # ... and in (2,1) and ... in (9,9).
    C1 = And([exactly1([S(r,c,n) for n in range(1,10)]) for r in range(1,10) for c in range(1,10) ])

    # Tasks 3-4
    # Every column/row has all numbers.

    # E.g. for columns this is saying:
    # exactly one of (1,1), (2,1), ... is number 1 for column 1,
    # and exactly one of (2,1), (2,2) ... is number 1 for column 2,
    # AND so on for all columns and numbers.

    # TASK 3: constraint for rows (or columns)
    C2 = And([exactly1([S(r,c,n) for r in range(1,10)]) for n in range(1,10) for c in range(1,10)]) #YOUR FORMULA HERE

    # TASK 4: constraint for columns (rows if you did columns in TASK 2).
    C3 = And([exactly1([S(r,c,n) for c in range(1,10)]) for n in range(1,10) for r in range(1,10)]) #YOUR FORMULA HERE

    # TASK 5 Implement the constraint for sub-squares.
    # Every 3X3 sub-grid has all numbers.
    # This should state that for all locations within the sub-square 1..3 x 1..3
    # there can be only a single number 1, AND within the sub-square 4..6 x 1.3
    # there can be only a single number 1, AND ...
    # so on for every sub-square and for every number.
    #
    # It is then a conjunction (And) of a long list of exactly1 over the sub-squares
    # for each number and for each sub-square.
    
    C4 = And([exactly1([S(3*r+i,3*c+j,n) for i in range(1,4) for j in range(1,4)]) for r in range(3) for c in range(3) for n in range(1,10)]) # YOUR FORMULA HERE

    # The solution respects the given clues
    C5 = And([S(r,c,puzzle[(r,c)]) for (r,c) in puzzle])

    return (C1,C2,C3,C4,C5)

### Print and display helper function
def sudoku2str(puzzle):
    """ 
    Produces a multi-line string representing a Sudoku board. 
    
    Fills in the number of a location if it is part of the puzzle or uses '.'
    if missing.

    Parameters
    ----------
    puzzle : dict of (row, column) : number
       The given Sudoku clues as the number for location (row, column).
        row, column, and number all in the range [1,9]
       A missing (row,column) key indicates that the number at that location
       is unknown.
   
    Returns
    -------
    str
       Multi-line string of the board.
    """
    board = ""
    for r in range(1,10):
        for c in range(1,10):
            if (r,c) in puzzle:
                board+= str(puzzle[(r,c)])
            else:
                board+='.'
            # After column 3 and 6 we put a grid divider, |
            if c in (3,6):
                board+='|'
        # Newline after each row.
        board+='\n'
        # And a divider line after row 3 and 6.
        if r in (3,6):
            board+="===|===|===\n"
    return board

# Solver function
def solve_sudoku(formulas):
    """
    Attempts to solve a Sudoku instance given formulas.

    Parameters
    ----------
    formulas : tuple (or list)
       These are the formulas describing the Sudoku instance, e.g. as returned
       by `sudoku2fma`.
    
    Returns
    -------
    dict of (row,column) : number or None
       None if no solution is found, or a solution in the form of a dictionary
       mapping from row,column pairs to the number at that location.
    """
    # Create z3 solver
    s = Solver()
    # Add formulas.
    s.add(formulas)
    if s.check() != sat:
        # There is no solution!
        return None
    # There's a solution, get a model and reconstruct the puzzle.
    m = s.model()
    # Now we have to check which of the atoms (i.e Boolean constants -
    # see function `S` above) is True, this indicates that the solution
    # has the number at that row,col coordinate.
    solution = {} # We'll place the solution in this dict.
    for r in range(1,10):
        for c in range(1,10):
            for n in range(1,10):
                # Reconstruct the atom and evaluate it in the model.
                # If true it means that that number is on that location, and
                # we add it to the model.
                if m.evaluate(S(r,c,n)) == True:
                    solution[(r,c)] = n
    return solution

if __name__ == "__main__":
    print("Example Sudokus. These should all take at most a few seconds each to solve.")
    print("---------------------------------------------------------------------------")
    print("AN EASY SUDOKU")
    print("--------------\n")
    # The easy ones are solved almost without search, just by performing
    # unit propagation. A little bit harder ones require from humans looking
    # ahead at the possibilities, and this means case analysis on at least
    # some of the propositional variables.
    
    puzzle0 = {(8, 1): 9, (6, 1): 8, (5, 2): 4, (1, 2): 5, (9, 3): 4, (7, 3): 8, (6, 3): 5, (2, 3): 9, (1, 3): 3, (7, 4): 9, (6, 4): 1, (4, 4): 4, (3, 4): 5, (2, 4): 7, (7, 5): 3, (2, 5): 8, (7, 6): 1, (6, 6): 9, (4, 6): 6, (3, 6): 3, (2, 6): 2, (9, 7): 8, (7, 7): 4, (6, 7): 3, (2, 7): 6, (1, 7): 7, (5, 8): 6, (1, 8): 9, (8, 9): 6, (6, 9): 2}
        
       
    print(sudoku2str(puzzle0))
    puzzle0fma = sudoku2fma(puzzle0)
    p0sol = solve_sudoku(puzzle0fma)
    if None == p0sol:
        print("No solution found [There should be one]!")
    else:
        print(sudoku2str(p0sol))

    print("-------------------------------------------------------------------\n")
    print("SUDOKU FROM LECTURE")
    print("-------------------\n")
    puzzle1 = {(7, 1): 3, (2, 1): 4, (8, 2): 5, (3, 2): 2, (6, 3): 1, (5, 3): 8, (9, 4): 8, (8, 4): 1, (7, 4): 4, (6, 5): 9, (4, 5): 5, (9, 6): 6, (7, 7): 2, (5, 7): 3, (4, 7): 4, (1, 8): 1, (4, 9): 7}
    
    print(sudoku2str(puzzle1))
    puzzle1fma = sudoku2fma(puzzle1)
    p1sol = solve_sudoku(puzzle1fma)
    if None == p1sol:
        print("No solution found [There should be one]!")
    else:
        print(sudoku2str(p1sol))

    print("-------------------------------------------------------------------\n")
    print("ARTO INKALA'S 'WORLD'S HARDEST SUDOKU'")
    print("--------------------------------------\n")
    puzzle2 = {(1, 1): 8, (9, 2): 9, (4, 2): 5, (3, 2): 7, (8, 3): 8, (7, 3): 1, (2, 3): 3, (8, 4): 5, (6, 4): 1, (2, 4): 6, (5, 5): 4, (3, 5): 9, (5, 6): 5, (4, 6): 7, (9, 7): 4, (5, 7): 7, (3, 7): 2, (8, 8): 1, (7, 8): 6, (6, 8): 3, (7, 9): 8}

    print(sudoku2str(puzzle2))
    puzzle2fma = sudoku2fma(puzzle2)
    p2sol = solve_sudoku(puzzle2fma)
    if None == p2sol:
        print("No solution found [There should be one]!")
    else:
        print(sudoku2str(p2sol))

         
