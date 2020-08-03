import unittest

from mcs import mc_trial, mc_execute
from gamestate import GameState
from pursuitstate import PursuitState


class TestMCS(unittest.TestCase):
    """
    Basic mcs_trial tests.
    """

    def test_1_return(self):
        """ Check that mc_trial returns a float value."""
        s = Zplus(v=0)
        v = mc_trial(0, s, 10)
        self.assertIsNotNone(v, "Did you forget the return statement?")
        self.assertEqual(v, 10, "Are you checking steps_left properly?")  # Should always be 10 as no options.

    def test_2_alternate(self):
        """ Check that mc_trial alternates between players. """
        s = Z0(v=0)
        v = mc_trial(0, s, 1)
        self.assertEqual(-1, v, "mc_trial with only one step failing.")
        v = mc_trial(0, s, 2)
        self.assertEqual(0, v, "Is the player being swapped in calls to mc_trial?")
        v = mc_trial(0, s, 3)
        self.assertEqual(-1, v, "Is the player being swapped in calls to mc_trial?")

    def test_3_random_action(self):
        """ Check that the action is picked uniformly at random. """
        s = ZCoin(v=0)
        N = 10000
        r = {1: 0, -1: 0}
        for _ in range(N):
            v = mc_trial(0, s, 1)
            r[v] += 1
        self.assertLess(abs(r[1] - r[-1]), 0.1 * N,
                        "Out of {N} tries your mc_trial picks action +1 {r[1]} times and action -1 {r[-1]} times. The "
                        "difference indicates that (unless you are quite unlucky) you may not pick the action uniform "
                        "at random.")

    def test_4_grid(self):
        """ Check that robber is captured in PursuitState."""
        testgrid3 = PursuitState(3, 3, [[0, 0, 0, 0],
                                        [0, 0, 0, 0],
                                        [0, 0, -1, 0],
                                        [1, 0, 0, 0]],
                                 0, 0, 3, 0, 0)
        v = mc_execute(0, testgrid3, 30, 2000)
        self.assertGreaterEqual(v, 0)


class Zplus(GameState):
    """ Integer test class with only action being +1 """

    def __init__(self, v=0):
        self.v = v

    def value(self):
        return self.v

    def applicable_actions(self, player):
        """ Always one action, regardless of player."""
        return [1]

    def successor(self, player, x):
        return Zplus(self.v + x)


class Z0(GameState):
    """ 
    Integer test class with actions being -1 for player 0, and +1 for 
    player 1 
    """

    def __init__(self, v=0):
        self.v = v

    def value(self):
        return self.v

    def applicable_actions(self, player):
        """ -1 for player 0, +1 for player 1."""
        return [-2 * (1 - player) + 1]

    def successor(self, player, x):
        return Z0(self.v + x)


class ZCoin(GameState):
    """ 
    Integer test class with actions being -1 +1 for both players.
    """

    def __init__(self, v=0):
        self.v = v

    def value(self):
        return self.v

    def applicable_actions(self, player):
        return [-1, 1]

    def successor(self, player, x):
        return Z0(self.v + x)


if __name__ == "__main__":
    unittest.main()
