import unittest

from qlearn import *
from gridmdp import GridMDP
from gridactions import *
from utils import follow_pi

class TestQLearning(unittest.TestCase):
    """
    Test value_best_action.
    """
    def setUp(self):
        self.gdp0 = GridMDP(["#*#",
                             "#.#",
                             "###"],
                            tile_rewards = {'*' : 20})
        # Made-up Q
        gdp0a = self.gdp0._Actions
        self.Q0 = {(0, 1): {gdp0a.east : 35,
                            gdp0a.south: 31,
                            gdp0a.west: 36,
                            gdp0a.north: 37,
                            gdp0a.remain: 40},
                   (1, 1): {gdp0a.east: 25,
                            gdp0a.south: 14,
                            gdp0a.west: 11,
                            gdp0a.north: 38,
                            gdp0a.remain: 12}}
        
        self.gdp1 = GridMDP(["-*-#",
                             "...#",
                             "...#",
                             "####"],
                            tile_rewards = {'*':20, '-':-1},
                            no_move_reward = -1)

        self.gdp2 = GridMDP(["#######",
                             "##...##",
                             "#..#..#",
                             "#..#..#",
                             "#..#.*#"],
                            tile_rewards = {'*':20})

        self.gdp3 = GridMDP(["#######",
                             "##...##",
                             "#..#..#",
                             "#.....#",
                             "#..#.*#"],
                            tile_rewards = {'*':20})



    def test_1_return(self):
        """Check that value_best_action returns a correct value."""
        mm = ManhattanMoves(1,2)
        Q = {(0,0) : {mm.north : 1.0, mm.south : 1.1,
                      mm.east : -1.2, mm.west : 0.0},
             (0,1) : {mm.north : 1.2, mm.south : 1.1,
                      mm.east : -1.2, mm.west : 0.0}}
        b1 = value_best_action((0,0), Q)
        b2 = value_best_action((0,1), Q)
        self.assertEqual(b1,1.1)
        self.assertEqual(b2,1.2)

    def test_2_make_policy(self):
        """Check that make_policy returns a correct policy."""
        pi = make_policy(self.gdp0,self.Q0)
        # Make sure it returns a non-empty dict.
        self.assertIsNotNone(pi)
        self.assertNotEqual(0,len(pi))
        # Same reward for going north as remaining in this particular case.
        self.assertEqual(pi[(0,1)],self.gdp0._Actions.remain)
        # Always need to take a step north here.
        self.assertEqual(pi[(1,1)],self.gdp0._Actions.north)

    def test_3_execute(self):
        """Check that execute reruns a correct value/distribution."""
        S = {(0,1) : 0,
             (1,0) : 0,
             (1,1) : 0,
             (1,2) : 0,
             (2,1) : 0}
        R = {(0,1) : 0,
             (1,0) : 0,
             (1,1) : 0,
             (1,2) : 0,
             (2,1) : 0}
        N = 10000
        for _ in range(N):
            s,r = execute(self.gdp1, (1,1), self.gdp1._Actions.north)
            S[s] += 1
            R[s] += r
        self.assertEqual(R[(0,1)]/S[(0,1)],20)
        self.assertAlmostEqual(S[(0,1)]/N,0.8,places=1)
        self.assertAlmostEqual(S[(1,0)]/N,0.1,places=1)
        self.assertAlmostEqual(S[(1,2)]/N,0.1,places=1)

    def test_4_q_learning_1(self):
        """ Check q_learning with gdp1. """
        Q = q_learning(self.gdp1,0.85,0.1,20000, start_state = (2,1))
        pi = make_policy(self.gdp1,Q)
        self.assertEqual(2,follow_pi(pi,(2,1),(0,1),self.gdp1))

    def test_5_q_learning_2(self):
        """ Check q_learning with gdp2. """
        Q = q_learning(self.gdp2,0.85,0.1,200000, start_state = (4,1))
        pi = make_policy(self.gdp2,Q)
        self.assertEqual(10,follow_pi(pi,(4,1),(4,5),self.gdp2))

    def test_6_q_learning_3(self):
        """ Check q_learning with gdp3. """
        Q = q_learning(self.gdp3,0.85,0.1,200000, start_state = (4,1))
        pi = make_policy(self.gdp3,Q)
        self.assertEqual(6,follow_pi(pi,(4,1),(4,5),self.gdp3))

    
        
if __name__ == "__main__":
    unittest.main()
