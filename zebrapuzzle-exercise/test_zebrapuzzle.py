import unittest
from zebrapuzzle import *
from z3 import sat,unsat,Solver, QuantifierRef

class TestZebra(unittest.TestCase):
    """
    Test the Zebra Puzzle constraints.
    """

    def test_task_1(self):
        """
        pets_diff: Quantifier expression that two different people must have different pets.
        """
        self.assertEqual(type(pets_diff), QuantifierRef, "pets_diff must be a quantifier expression.")
        s = Solver()
        s.add(pets_diff)
        # Counter-example
        s.add(KeepsPet(ukr) == horse)
        s.add(KeepsPet(nor) == horse)
        self.assertEqual(unsat, s.check(), "Two different persons should not be able to have the same pet.")

    def test_task_2(self):
        """
        drinks_diff: Quantifier expression that two different people must drink different beverages.
        """
        self.assertEqual(type(drinks_diff), QuantifierRef, "drinks_diff must be a quantifier expression.")
        s = Solver()
        s.add(drinks_diff)
        # Counter-example
        s.add(Drinks(eng) == milk)
        s.add(Drinks(spa) == milk)
        self.assertEqual(unsat, s.check(), "Two different persons should not be able to drink the same beverage.")

    def test_task_3(self):
        """
        stmt4 : The Ukrainian must drink tea.
        """
        s = Solver()
        s.add(stmt4)
        # Counter-example
        s.add(Drinks(ukr) == coffee)
        self.assertEqual(unsat, s.check(), "The Ukrainian should not be able to drink anything else than tea.")

    def test_task_5(self):
        """
        stmt5 : The green house must be located immediately to the right of the ivory house.
        """
        s = Solver()
        s.add(stmt5)
        # Counter-example
        s.add(NumberOf(green) == 4)
        s.add(NumberOf(ivory) == 5)
        self.assertEqual(unsat, s.check(), "It must not be possible to place the green house anywhere but immediately to the right of the ivory house.")

    def test_task_6(self):
        """
        stmt7: Quantifier expression that Kools are smoked in the yellow house.
        """
        self.assertEqual(type(stmt7), QuantifierRef, "stmt7 must be a quantifier expression (Exists/ForAll).")
        s = Solver()
        s.add(stmt7)
        s.add(house_nums,brands_diff, colors_diff) # Additional constraints
        # Counter-example (one of many)
        s.add(Or(And(LivesIn(ukr) == NumberOf(yellow), Smokes(ukr) == ls),
                  And(LivesIn(nor) == NumberOf(green), Smokes(nor) == ko)))
        
        self.assertEqual(unsat, s.check(), "It is possible for some person to live in the yellow house and smoke something else than Kools, or to smoke Kools and live in a non-yellow house.")

    def test_task_7(self):
        """
        stmt10: Quantifier expression that the man who smokes chesterfields lives in the house next to the man with the fox.
        """
        self.assertEqual(type(stmt10), QuantifierRef, "stmt10 must be a quantifier expression (Exists/ForAll).")
        s = Solver()
        s.add(stmt10)
        s.add(house_nums,brands_diff,pets_diff) # Additional constraints
        # Counter-examples (one of many)
        s.add(LivesIn(ukr) == 3, LivesIn(spa) == 4, LivesIn(nor) == 5,
              KeepsPet(spa) == fox, Smokes(ukr) == ls, Smokes(nor) == og)
        self.assertEqual(unsat, s.check())

    def test_task_8(self):
        """
        stmt11: Quantifier expression that Kools are smoked next to the house where the horse is kept.
        """
        self.assertEqual(type(stmt11), QuantifierRef, "stmt11 must be a quantifier expression (Exists/ForAll).")
        s = Solver()
        s.add(stmt11)
        s.add(house_nums,brands_diff,pets_diff) # Additional constraints
        # Counter-examples (one of many)
        s.add(LivesIn(ukr) == 3, LivesIn(spa) == 4, LivesIn(nor) == 5,
              KeepsPet(ukr) == horse, Smokes(nor) == ko),
        self.assertEqual(unsat, s.check())

    def test_task_9(self):
        """
        stmt13 : The Japanese smokes Parliaments.
        """
        s = Solver()
        s.add(stmt13)
        # Counter-example
        s.add(Smokes(jap) == og)
        self.assertEqual(unsat, s.check(), "It must not be possible for the Japanese man to smoke anything bug Parliaments.")


    def test_z_puzzle(self):
        """
        Check if a solution is possible given the constraints.
        This test will succeed with too lax constraints and fail if the 
        constraints are too rigid.

        Thus it may be the only test which passes initially, but might then 
        start failing as the other tasks are completed.
        """
        s = Solver()
        s.add(house_nums, colors_diff, brands_diff, drinks_diff, pets_diff,
              stmt1, stmt2, stmt3, stmt4, stmt5, stmt6, stmt7,stmt8,stmt9,stmt10,
              stmt11, stmt12,stmt13,stmt14)
        self.assertEqual(sat, s.check(), "One or more tasks possibly expressing too rigid constraints.")
        
if __name__ == "__main__":
    unittest.main()


