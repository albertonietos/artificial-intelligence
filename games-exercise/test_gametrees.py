import unittest
from tictactoestate import *

from gametrees import *

import math

class TestMiniMax(unittest.TestCase):
    """
    Test the minimax function.
    """

    def test_1_return(self):
        """ Check that minimax returns a value."""
        s = TicTacToeState()
        v = minimax(0,s,1)
        self.assertIsNotNone(v, "Did you forget the return statement?")
        self.assertEqual(v,0, "Needs to return the value of the final state.") # Always zero as there is not enough moves to finish.

    def test_2_calls(self):
        """ Check that minimax performs 82 (= 1 +9 + 9*8) minimax calls with an initial depth of 2."""
        s = TicTacToeState()
        minimax.calls = 0
        v = minimax(0,s,2)
        # A depth of 2 there should be 1 + 9 + 9*8 = 82 minimax calls.
        self.assertEqual(minimax.calls,82)

    def test_3_draw(self):
        """ Check that tictactoe results in a draw with minimax. """
        s = TicTacToeState()
        v = minimax(0,s,10)
        self.assertEqual(v,0)
        
class TestAlphaBeta(unittest.TestCase):
    """
    Test the alphabeta function.
    """

    def test_1_return(self):
        """ Check that alphabeta returns a value."""
        s = TicTacToeState()
        v = alphabeta(0,s,1,-math.inf,math.inf)
        self.assertIsNotNone(v, "Did you forget the return statement?")
        self.assertEqual(v,0, "Needs to return the value of the final state.") # Always zero as there is not enough moves to finish.

    def test_2_calls(self):
        """ Check that alphabeta performs 26 alphabeta calls with an initial depth of 2."""
        s = TicTacToeState()
        alphabeta.calls = 0
        v = alphabeta(0,s,2,-math.inf,math.inf)
        # A depth of 2 there should be 26 alphabeta calls.
        # If you have forgotten
        self.assertEqual(alphabeta.calls,26, "If you have 82 calls here, check that you break at alpha >= beta.")

    def test_3_draw(self):
        """ Check that tictactoe results in a draw with alphabeta. """
        s = TicTacToeState()
        v = alphabeta(0,s,10,-math.inf,math.inf)
        self.assertEqual(v,0)



if __name__ == "__main__":
    unittest.main()
