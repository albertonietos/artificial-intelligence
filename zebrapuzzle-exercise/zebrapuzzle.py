"""
Solves the zebra puzzle (https://en.wikipedia.org/wiki/Zebra_Puzzle) using the z3 SMT library.
"""

# Besides the import statements and helper function
# declarations just below, this source file has three main 'sections':
# - First we declare the sorts, i.e. the types making up the universe.
# - Then we declare functions, which maps between the sorts.
# - Finally, we create predicates constraining the problem
#
# Last in the file, the __main__ routine will add all constraints to a solver
# and attempt to find and print a model.

from z3 import And, Or, Not, Implies, Solver, sat, Function, EnumSort, ForAll, \
    Exists, Xor, If, IntSort, Const

# ----------- Helper functions

# Helper function - define our own absolute value formula.
# Look at `stmt14` below to see an example of how it is used.
def zabs(x):
    """
    Gives a z3 expression equivalent of abs(x) - the absolute value of x.
    Helper function. Use this as you would for abs but in formulas.
    
    Parameters
    ----------
    x : z3.ArithRef
        A z3 arithmetic expression, or a number.
    
    Returns
    -------
    z3 formula
        If(x >= 0, x, -x) which expresses a sign change for negative z3 arithmetic values.
    """
    return If(x >= 0,x,-x)

def format_model(m):
    """
    Prepares a string-table of each house-inhabitant given a model.

    Parameters
    ----------
    m : z3 model
       An answer to the puzzle.

    Returns
    -------
    str
       Multi-line string of the model.
    """
    cnum = {m.evaluate(NumberOf(c)).as_long() : c for c in (red,green,ivory,blue,yellow)}
    pnum = {m.evaluate(LivesIn(p)).as_long() : p for p in (jap,nor,spa,ukr,eng)}
    ss = ["House {0} is {1}. The inhabitant is {2}, drinks {3}, smokes {4}, and has pet {5}."\
          .format(h, cnum[h], pnum[h], m.evaluate(Drinks(pnum[h])),
                  m.evaluate(Smokes(pnum[h])),
                  m.evaluate(KeepsPet(pnum[h]))) for h in range(1,6)]
    return "\n".join(ss)
        


# ----------- SORTS: Declaring the universe.
# EnumSort used to define symbols

# Corresponds to 'M' in the lecture
Person, (eng, jap, nor, spa, ukr) = EnumSort('Person', ('English', 'Japanese',
                                                        'Norwegian', 'Spanish',
                                                        'Ukrainian'))
# Houses are numbered; So they are of Integer Sort.
# We need house "numbers" in order to be able to view them as a
# row, and thus talk about concepts such as "to the right of".
HouseNum = IntSort() # Corresponds to 'H' in the lecture.

# Corresponds to 'C' in the lecture
Brand, (og, ko, ch, ls, pa) = EnumSort('Brand', ('OldGold', 'Kools',
                                                   'Chesterfields',
                                                   'LuckyStrike',
                                                   'Parliaments'))

# Corresponds to 'P' in the lecture
Col, (red, green, ivory, yellow, blue) = EnumSort('Col', ('Red', 'Green',
                                                                'Ivory',
                                                                'Yellow',
                                                                'Blue'))

# Corresponds to 'A' in the lecture
Animal, (dog, snails, fox, horse, zebra) = EnumSort('Animal', ('dog', 'snails',
                                                               'fox', 'horse',
                                                               'zebra'))
# Corresponds to 'D' in the lecture
Beverage, (coffee, tea, milk, oj, water) = EnumSort('Beverage', ('coffee', 'tea',
                                                                 'milk',
                                                                 'OrangeJuice',
                                                                 'water'))


# -------------- FUNCTIONS: mapping between types (sorts).


# This section declares functions on the Sorts defined above.
# These functions can then be used to write predicates.
# For example, the predicate 'Drinks(Ukr, Tea)' (which is true if
# the Ukrainian drinks tea), is written as Drinks(ukr) == tea
# here, using the function Drinks (declared below).

# Who drinks what? Drinks is a function from Person to Beverage.
Drinks = Function('Drinks', Person, Beverage)

# Who smokes what?
Smokes = Function('Smokes', Person, Brand)

# Who lives in which house number?
LivesIn = Function('LivesIn', Person, HouseNum)

# Gets the number of a house with some color.
# So e.g. Predicate Color(3,Green) is written
# NumberOf(Green) == 3
NumberOf = Function('NumerOf', Col, HouseNum)

# Who has what animal as a pet?
KeepsPet = Function('KeepsPet', Person, Animal)


# -------------- PREDICATES: encoding the puzzle and constraining the solution

# First we declare a few variables to use in quantifier expressions.
# These are used in ForAll and Exists expressions to denote persons
# and house-colors. (For some examples, see below.)
# You can also use p1 and p2 in some of the expressions you'll write for your
# tasks further down.

p1 = Const('p1', Person)
p2 = Const('p2', Person)
c1 = Const('c1', Col)
c2 = Const('c2', Col)

# Now we start by encoding some general constraints: house numbering,
# that everyone has different pets, smokes different brands, and so on.

# The first part of the conjunction states that a person must live in a 
# house numbered between 1 and 5.
# The second part says that for every pair of persons, either
# the persons are the same or the numbers differ (it can not be both).
# The effect is that any satisfiable solution must allocate an unique
# number to every one of the five houses.
# The declaration makes use of the exclusive or, Xor operation (you will not need
# to use Xor in your tasks.)
house_nums = And(ForAll([p1], And(1 <= LivesIn(p1), LivesIn(p1) <= 5)),
                 ForAll([p1,p2], Xor(p1 == p2, LivesIn(p1) != LivesIn(p2))))

# If we adopt the convention that the houses are ordered 1..5 from left
# to right, then the predicate "The green house is in the middle" can
# now be written as `NumberOf(green) == 3`, and the predicate
#"The green house is next to the ivory house" as 
# `zabs(NumberOf(green) - NumberOf(ivory)) == 1`
# (their absolute difference is exactly 1).

# We also need to say that each house has a unique color.
# This can be achieved in a few different ways, but here we say that for
# every two people, they are either the same, or there are two houses
# of different colors where they live.
colors_diff = ForAll([p1,p2], Xor(p1 == p2, Exists([c1,c2],And(c1!=c2,
                                                              NumberOf(c1) == LivesIn(p1),
                                                              NumberOf(c2) == LivesIn(p2)))))

# That each person smokes a different brand...
# (We can re-use p1 and p2 declared above).
# Using the quantifier ForAll, we now say that for all values of p1 and p2,
# if p1 and p2 are different persons it follows that they smoke different
# brands.
brands_diff = ForAll([p1,p2], Implies(p1 != p2, Smokes(p1) != Smokes(p2)))

# Keeps different pets
pets_diff = ForAll([p1,p2], Implies(p1 != p2, KeepsPet(p1) != KeepsPet(p2))) # TASK 1: Replace True with a quantifier z3 expression. Hint: see brands_diff.

# And drinks different drinks
drinks_diff = ForAll([p1, p2], Implies(p1 != p2, Drinks(p1) != Drinks(p2))) # TASK 2: Replace True with a quantifier z3 expression. Hint: see brands_diff.


# Let's encode the puzzle:
# -----------------------
#

# The Englishman lives in the red house.
stmt1 = LivesIn(eng) == NumberOf(red)

# The Spaniard owns the dog.
stmt2 = KeepsPet(spa) == dog

# Coffee is drunk in the green house.
stmt3 = Exists([p1], And(Drinks(p1)==coffee, LivesIn(p1)==NumberOf(green) ) )

# The Ukrainian drinks tea.
stmt4 = Drinks(ukr) == tea # TASK 3: Replace True with the z3 expression for the above statement.

# The green house is immediately to the right of the ivory house.
stmt5 = (NumberOf(green) - NumberOf(ivory)) == 1 # TASK 4: Replace True with the z3 expression for the above statement.
# Hint: remember that the houses are numbered 1 .. 5 from left to right.

# The Old Gold smoker owns snails.
stmt6 = Exists([p1], And(Smokes(p1) == og, KeepsPet(p1) == snails))

# Kools are smoked in the yellow house.
stmt7 = Exists([p1], And(Smokes(p1) == ko, LivesIn(p1) == NumberOf(yellow))) # TASK 5: Replace True with a z3 Quantifier (Exists/ForAll) expression
# for the above statement.
# Hint: Look at stmt6 and stmt1.
# Think: "There is some person who ... and lives in a house which ...."
      
# Milk is drunk in the middle house.
stmt8 = Exists([p1], And(Drinks(p1) == milk, LivesIn(p1) == 3)) # TASK 6: Replace True with the z3 Quantifier (Exists/ForAll) expression
# for the above statement.

# The Norwegian lives in the first house. (I.e house number 1.)
stmt9 = LivesIn(nor) == 1

# The man who smokes Chesterfields lives in the house next to the man with the fox.
stmt10 = Exists([p1, p2], And(Smokes(p1) == ch, KeepsPet(p2) == fox, zabs(LivesIn(p1)-LivesIn(p2)) == 1)) # TASK 7: Replace True with the z3 Quantifier (Exists/ForAll) expression
# for the above statement.
# Hint: You will need a quantifier over both p1 and p2 to be able to talk of two
# different persons.

# Kools are smoked in the house next to the house where the horse is kept.
stmt11 = Exists([p1, p2], And(Smokes(p1)==ko, KeepsPet(p2)==horse, zabs(LivesIn(p1)-LivesIn(p2))==1)) # TASK 8: Replace True with the z3 Quantifier (Exists/ForAll)
# expression for the above statement.
# Hint: You will need a quantifier over both p1 and p2 to be able to talk of two
# different persons.

# The Lucky Strike smoker drinks orange juice.
stmt12 = Exists([p1], And(Smokes(p1) == ls, Drinks(p1) == oj))

# The Japanese smokes Parliaments.
stmt13 = Smokes(jap) == pa # TASK 9: Replace True with the z3 expression for the above statement.

# The Norwegian lives next to the blue house.
stmt14 = zabs(LivesIn(nor) - NumberOf(blue)) == 1


if __name__ == "__main__":
    # Create solver
    s = Solver()
    # Add all the constraints.
    # To debug the influence of some specific constraint you could
    # add only the ones you are interested in here, or as this is a
    # conjunction of all constraints, set the ones you are not interested
    # in to `True` above.
    s.add(house_nums, colors_diff, brands_diff, drinks_diff, pets_diff,
          stmt1, stmt2, stmt3, stmt4, stmt5, stmt6, stmt7,stmt8,stmt9,stmt10,
          stmt11, stmt12,stmt13,stmt14)
    print("Checking for a model given the constraints (may take a little bit of time)...")
    if(sat == s.check()):
        print("The model found is:")
        print(format_model(s.model()))
    else:
        print("No model found (unsat). Check your statements.")
        
