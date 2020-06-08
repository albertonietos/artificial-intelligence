"""Tests for knightsstate.py"""

import unittest
from knightsstate import KnightsState


class TestKnightsStateSuccessors(unittest.TestCase):
    """
    Test successor function.
    """

    def test_0_return(self):
        """Successors should return something."""
        ks = KnightsState([])
        succ = list(ks.successors())
        self.assertNotEqual(succ, None,
                            "Hint: Did you remember the return statement?")

    def test_1_empty(self):
        """There should be no successor states from the empty board."""
        ks = KnightsState([])
        succ = list(ks.successors())
        self.assertEqual(0,len(list(succ)))

    def test_2_full(self):
        """There should be no successor states from a filled board."""
        ks = KnightsState([(r,c) for r in range(8) for c in range(8)])
        succ = list(ks.successors())
        self.assertEqual(0,len(list(succ)))

    def test_3_all_legal(self):
        """One piece with no obstructed moves will have all eight possible successors present."""
        ks = KnightsState([(4,4)])
        sas = list(ks.successors()) # Get a list of successors
        _,succ = zip(*sas) # Transpose the answer to get list of states.
        # These are the eight possible successor states.
        truth = [KnightsState([(3,6)]),
                 KnightsState([(5,6)]),
                 KnightsState([(2,5)]),
                 KnightsState([(6,5)]),
                 KnightsState([(3,2)]),
                 KnightsState([(5,2)]),
                 KnightsState([(2,3)]),
                 KnightsState([(6,3)])]

        # Check for same number of successors
        self.assertEqual(len(truth),len(list(succ)))
        # Then check that all of the successors are present in result.
        for t in truth:
            self.assertIn(t, succ)
        # Finally check the actions.
        self.assertTrue(all(a.source in ks.occupied and a.target in s.occupied \
                            for a,s in sas), "Actions do not match.")
                          
    def test_4_no_move_outside(self):
        """Successors are only made up from moves within the board."""
        ks = KnightsState([(0,0)])
        sas = list(ks.successors()) # Get a list of successors
        _,succ = zip(*sas) # Transpose the answer to get list of states.
        # These are the possible successors.
        truth = [KnightsState([(1,2)]),
                 KnightsState([(2,1)])]
        hint = "Hint: Are you making sure that a move does not end up outside the board?"
        # Check for same number of successors
        self.assertEqual(len(truth),len(list(succ)), hint)
        # Then check that all of the successors are present in result.
        for t in truth:
            self.assertIn(t, succ, hint)
        # Finally check the actions.
        self.assertTrue(all(a.source in ks.occupied and a.target in s.occupied \
                            for a,s in sas), "Actions do not match.")

    def test_5_no_moves_to_occupied(self):
        """Successors are only made up from moves to unoccupied locations."""
        ks = KnightsState([(5,6), (7,7)])
        sas = list(ks.successors()) # Get a list of successors
        _,succ = zip(*sas) # Transpose the answer to get list of states.
        # These are the possible successors.
        truth = [KnightsState([(5,6), (6,5)]),
                 KnightsState([(3,7), (7,7)]),
                 KnightsState([(4,4), (7,7)]),
                 KnightsState([(6,4), (7,7)]),
                 KnightsState([(3,5), (7,7)]),
                 KnightsState([(7,5), (7,7)])]
        hint = "Hint: Are you making sure that a move does not end up in an already occupied location?"
        # Check for same number of successors
        self.assertEqual(len(truth),len(list(succ)), hint)
        # Then check that all of the successors are present in result.
        for t in truth:
            self.assertIn(t, succ, hint)
        # Finally check the actions.
        self.assertTrue(all(a.source in ks.occupied and a.target in s.occupied \
                            for a,s in sas), "Actions do not match.")

    def test_6_only_one_move(self):
        """Only a single move should be made between a start state an each of its successors."""
        occ = [(5,7), (0,1), (4,2)]
        ks = KnightsState(occ)
        _,succ = zip(*ks.successors()) # Transpose the answer to get list of states.
        # Go over each successor state
        for ss in succ:
            # The set intersection of occupied spaces should be one less than
            # the total number of pieces in the board, meaning that only one
            # piece has been moved from one place to another.
            self.assertEqual(len(ks.occupied.intersection(ss.occupied)),
                             len(occ)-1,
                             "Hint: Only one piece on the board may move in a single action.")

class TestKnightsStateBasics(unittest.TestCase):
    """
    Test non student-task related code. 
    """
    
    def test_init(self):
        """Just test that the occupied parameter is copied."""
        # Couple of locations
        occ1 = [(3,3),(1,2)]
        # KnightsState
        ks1 = KnightsState(occ1)
        # Should have the same locations as when created.
        self.assertEqual(frozenset(occ1),ks1.occupied)

        # Add a repeated location
        occ2 = occ1 + [(3,3)]
        # New knights state
        ks2 = KnightsState(occ2)
        # The repeated location should be removed, and
        # the occupied locations of ks2 should be the same
        # as the set of locations in occ1.
        self.assertEqual(frozenset(occ1),ks2.occupied)
        
    def test_init_fail(self):
        """ Test that non-board locations raises an exception."""
        with self.assertRaises(ValueError):
            KnightsState([(-1,0)])
        with self.assertRaises(ValueError):
            KnightsState([(0,8)])
        with self.assertRaises(TypeError):
            KnightsState([(0,1.1)])

    def test_equality(self):
        """ Test that two objects are equal if they represent the same board,
        otherwise not.
        """
        occ1 = [(4,5),(2,2)]
        occ2 = [(5,4),(2,2)]

        ks1a = KnightsState(occ1)
        ks1b = KnightsState(occ1)
        self.assertEqual(ks1a,ks1b)

        ks2 = KnightsState(occ2)
        self.assertNotEqual(ks2,ks1a)
        
if __name__ == "__main__":
    unittest.main()
