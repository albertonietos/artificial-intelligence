import unittest
from knightsknaves import *
from z3 import sat,unsat,Solver,QuantifierRef,And,ExprRef

class TestKnightsKnaves(unittest.TestCase):
    """
    Test the task functions of knightsknaves.py.
    
    Note: These are basic tests simply looking at satisfiability.
 
    Failing the test means that the implementation is wrong, but passing does not
    guarantee correctness.

    Make sure to solve the puzzle yourself and check the printed output.
    """

    def test_knaves_1(self):
        """
        `knaves_tell_lies` must return a formula based on the ForAll quantifier (type QuantifierRef).
        """
        f = knaves_tell_lies()
        self.assertIsNotNone(f, "Nothing returned by `knaves_tell_lies`.")
        self.assertIsInstance(f, QuantifierRef, "Hint: Look at `knights_tell_truths`.")
        
    def test_knaves_2(self):
        """
        The formula returned by `knaves_tell_lies` and a lying knave must be satisfiable.
        """
        f = knaves_tell_lies()
        s = Solver()
        s.add(f)
        s.add(And(R(A) == Knave, S(A) == False))
        self.assertEqual(sat,s.check(), "Your formula should say that being a knave implies not telling the truth for all persons.")
        
    def test_knaves_3(self):
        """
        It can not be that a person has the role of a knave and tells the truth.
        """
        f = knaves_tell_lies()
        s = Solver()
        s.add(f)
        s.add(And(R(C) == Knave, S(C) == True))
        self.assertEqual(unsat,s.check(), "Your formula should say that being a knave implies not telling the truth for all persons.")

    
    def test_puzzle_task_1(self):
        """
        `puzzle_task` must return dictionary with one z3 formula (type ExprRef) for each of (A,B,C).
        """
        d = puzzle_task()
        self.assertIsNotNone(d, "Nothing (None) returned by `puzzle_task`. It should return a dictionary.")
        for p in (A,B,C):
            self.assertTrue(p in d, f"No statement for person {p} in dictionary.")
            self.assertIsInstance(d[p], ExprRef)

    def test_puzzle_task_2(self):
        """
        The puzzle should be solvable.
        """
        claims = puzzle_task()
        stmts = encode_statements(claims)
        s = Solver()
        d1 = abc_different()
        d2 = knights_tell_truths()
        d3 = knaves_tell_lies()
        s.add(d1,d2,d3,stmts)
        # This should be satisifable
        self.assertEqual(sat, s.check(), "Puzzle is not solvable.")
        
if __name__ == "__main__":
    unittest.main()
