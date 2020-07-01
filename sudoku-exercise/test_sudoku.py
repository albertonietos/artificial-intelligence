import unittest
from sudoku import *
from z3 import BoolVal,sat,unsat,Solver

def check(solution):
    """ 
     Rough check if a solution is valid.
     
     Parameters
     ----------
     solution : dict of (row, column) : number
        The given Sudoku clues as the number for location (row, column).
        row, column, and number all in the range [1,9]
        A missing (row,column) key indicates that the number at that location
         is unknown.
    
     Returns
     -------
     tuple (bool,str)
       First in pair is True if OK, False if error.
       Second in pair is message.
     """
    if len(solution) != 9*9:
        return (False, "Solution is of wrong size, perhaps it is not complete?")
    if set(solution.values()) != set(range(1,10)):
        return (False, "Solution does not contain the numbers [1..9]. Some missing?")
    # Rough check that the distribution is correct. There should be 9 of each
    # number in [1,9] present.
    # More elaborate checks are possible by breaking down to rows, columns, and
    # sub-squares. This is done in the grader.
    for n in range(1,10):
        # Count occurrences of n in solution values.
        if 9 != sum(1 for x in solution.values() if x == n):
            return (False, "You do not have unique numbers in some row/column/sub-grid.")  
    return (True,"")

class TestSudoku(unittest.TestCase):
    """
    Test the Sudoku-implementation.
    """
    def test_1_atMost1(self):
        # The easiest formulas imaginable is the boolean values True and False,
        # use these to test.
        # Two values, both false.
        fmas = [BoolVal(False), BoolVal(False)]
        # Should be OK.
        s = Solver()
        s.add(atMost1(fmas))
        self.assertEqual(sat,s.check(), "Formula returned by atMost1 should be sat when all input formulas evaluate to False.")
        # Append a True value,
        fmas.append(BoolVal(True))
        # Should be OK.
        s = Solver()
        s.add(atMost1(fmas))
        self.assertEqual(sat,s.check(), "Formula returned by atMost1 should be sat when only one of the input formulas evaluates to True.")
         # Append another True value,
        fmas.append(BoolVal(True))
        # Should not be OK.
        s = Solver()
        s.add(atMost1(fmas))
        self.assertEqual(unsat,s.check(), "Formula returned by atMost1 should not be sat when more than one of the input formulae evaluates to True.")
        
    def test_2_exactly1(self):
        # The easiest formulas imaginable is the boolean values True and False,
        # use these to test.
        # Two values, both false.
        fmas = [BoolVal(False), BoolVal(False)]
        # Should not be OK.
        s = Solver()
        s.add(exactly1(fmas))
        self.assertEqual(unsat,s.check(), "Formula returned by exactly1 should not be sat when all input formulas evaluate to False.")
        # Append a True value,
        fmas.append(BoolVal(True))
        # Should be OK.
        s = Solver()
        s.add(exactly1(fmas))
        self.assertEqual(sat,s.check(), "Formula returned by exactly1 should be sat when only one of the input formulas evaluates to True.")
         # Append another True value,
        fmas.append(BoolVal(True))
        # Should not be OK.
        s = Solver()
        s.add(exactly1(fmas))
        self.assertEqual(unsat,s.check(), "Formula returned by exactly1 should not be sat when more than one of the input formulae evaluates to True.")
        
    def test_3_impossible_row(self):
        """
        There should be no solution (unsat) for an impossible row puzzle.
        It has no solution. If one is found your constraints are too lax.
        """
        puzzle = {(2,2) : 2, (2,7) : 2} # Two in the same row, anything else goes.
        fma = sudoku2fma(puzzle)
        s = Solver()
        s.add(fma)
        self.assertNotEqual(s.check(), sat, "Check your row constraints!")

    def test_4_impossible_col(self):
        """
        There should be no solution (unsat) for an impossible column puzzle.
        It has no solution. If one is found your constraints are too lax.
        """
        puzzle = {(2,2) : 2, (7,2) : 2} # Two in the same col, anything else goes.
        fma = sudoku2fma(puzzle)
        s = Solver()
        s.add(fma)
        self.assertNotEqual(s.check(), sat, "Check your column constraints!")
        
    def test_5_impossible_square(self):
        """
        There should be no solution (unsat) for an impossible sub-square puzzle.
        It has no solution. If one is found your constraints are too lax.
        """
        puzzle = {(2,2) : 2, (3,3) : 2} # Two in the same subsquare.
        fma = sudoku2fma(puzzle)
        s = Solver()
        s.add(fma)
        self.assertNotEqual(s.check(), sat, "Check your sub-square constraints!")


       
    def test_6_puzzle_0(self):
        """Puzzle example 0 should have a correct solution. 
        This is the same as 'AN EASY SUDOKU' in sudoku.py __main__
        If you have an error here, it is worth looking at the printed outputs
        when running that example for visual hints to which constraints might
        be wrong.
        """
        puzzle = {(8, 1): 9, (6, 1): 8, (5, 2): 4, (1, 2): 5, (9, 3): 4, (7, 3): 8, (6, 3): 5, (2, 3): 9, (1, 3): 3, (7, 4): 9, (6, 4): 1, (4, 4): 4, (3, 4): 5, (2, 4): 7, (7, 5): 3, (2, 5): 8, (7, 6): 1, (6, 6): 9, (4, 6): 6, (3, 6): 3, (2, 6): 2, (9, 7): 8, (7, 7): 4, (6, 7): 3, (2, 7): 6, (1, 7): 7, (5, 8): 6, (1, 8): 9, (8, 9): 6, (6, 9): 2}
        fma = sudoku2fma(puzzle)
        sol = solve_sudoku(fma)
        self.assertNotEqual(sol, None, "No solution found!")
        ok, msg = check(sol)
        self.assertTrue(ok,msg)
        
    def test_7_puzzle_1(self):
        """Puzzle example 1 should have a correct solution. 
        This is the same as 'SUDOKU FROM LECTURE' in sudoku.py __main__
        If you have an error here, it is worth looking at the printed outputs
        when running that example for visual hints to which constraints might
        be wrong.
        """
        puzzle = {(7, 1): 3, (2, 1): 4, (8, 2): 5, (3, 2): 2, (6, 3): 1, (5, 3): 8, (9, 4): 8, (8, 4): 1, (7, 4): 4, (6, 5): 9, (4, 5): 5, (9, 6): 6, (7, 7): 2, (5, 7): 3, (4, 7): 4, (1, 8): 1, (4, 9): 7}
        fma = sudoku2fma(puzzle)
        sol = solve_sudoku(fma)
        self.assertNotEqual(sol, None, "No solution found!")
        ok, msg = check(sol)
        self.assertTrue(ok,msg)

if __name__ == "__main__":
    unittest.main()

