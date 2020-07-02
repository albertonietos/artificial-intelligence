
from z3 import BoolSort,EnumSort,Function,Solver,sat,And,ForAll,Or,Xor,Distinct,Implies,Const,Not


# The knight-knave-spy puzzle speaks about three persons (A,B,C)
# and three roles (Knight,Knave,Spy).
# To be able to encode the puzzle statements we need to express predicates -
# functions - on these domains.
# So, first we declare two enum 'sorts'. In Z3 a 'sort' is like a type.
# EnumSort thus is a sort of enumerable many values. In this case, Knight,
# Knave, and Spy.

# The first is the name (Role) followed by a tuple of all values.
Role, (Knight, Knave, Spy) = EnumSort('Role', ('Knight', 'Knave', 'Spy'))

# Same for Person. Values A, B, C.
Person, (A,B,C) = EnumSort('Person', ('A', 'B', 'C'))

# Now, what we want to do is reconstruct who is who based on puzzle
# statements as predicates.
# Let's declare a function R which gives the role of a person.
# This is a function which maps from Person to Role:
R = Function('R', Person, Role)

# As you can see we have just declared a function - there's no 
# 'implementation' or code. This because if we know how to encode
# this function, the problem would be solved! (We would know who was
# who.) In fact, the function R is the unknown quantity, this is what
# our solver will reconstruct. So it is an unknown!

# But, as it is a z3 function, we can go ahead and write predicates
# using it. For example, R(A) != R(B)  would encode that the role of A cannot be
# the same as the role of B.

# In fact, the first general constraint of the game - that there is always one
# person of each sort - could be encoded in this manner:
# Saying "The role of A is not the same as the role of B, is not the same as role of C."
# Or in code as `And([R(A) != R(B), R(B) != R(C), R(C) != R(A)])`

# In fact, z3 has a built-in directive to state that a set of values must have
# unique values. It's called distinct, and can be used like this:
def abc_different():
    """
    R(A),R(B),R(C) must all have distinct values.

    Returns
    -------
    Formula
    """
    return Distinct([R(A), R(B), R(C)])

# The downside with the above is that we need explicitly encode the domain
# of R - {A,B,C} - which is OK for three values, but not if there would be
# thousands.
# Instead, if we wanted we could use a quantified formula to say the same thing.
# That is, ∀x, y : Xor(x = y, R(x) ≠ R(y))
# Either the two Persons x,y are equal or they have different roles.
#
# It is done like this:
def all_persons_have_different_roles():
    """
    Encode ∀x, y : Xor(x = y, R(x) ≠ R(y))
    Either the two Persons x,y are the same or they have different roles.

    This is an alternative to `abc_different`.

    Returns
    -------
    Formula
    """
    # We need to declare the variables fist.
    x = Const('x', Person) # This x defined on the domain of Person
    y = Const('y', Person) # And this is y
    return ForAll([x, y],Xor(x == y, R(x) != R(y))) # ForAll expression



# In addition to a function for the role of a person, we also need
# to be able to write predicates about a their statements in order
# to encode the essence of sentences such as "A lies", 
# and "That (referring to the previous speaker) is not true".
#
# To do that we use a function from Person to Bool which is True if
# the claim is that the person tells the truth, and False otherwise.
# Call it S : Person -> Bool
S = Function('S', Person, BoolSort())
# Here BoolSort() just says that the return type is of type Bool.


# Now using both R and S, we can encode the general rules of the game:

# 2, That a Knight must tell the Truth.
# For a specific person, say B this would be (R(B) = Knight) ⇒ S(B), encoded
# as Implies(R(B) == Knight, S(B)), but we use the ∀x quantifier 
# and write for all persons:
def knights_tell_truths():
    """
    Encodes 'Knights always tell the truth'.

    In other terms: for all persons, being a knight implies telling the truth.

    Returns
    -------
    Formula
   
    """
    # We need to declare the variables fist.
    x = Const('x', Person) # This x defined on the domain of Person
    return ForAll([x], Implies(R(x) == Knight, S(x)))


# 3, The same goes for Knaves - they always lie, 
# i.e. ∀x : R(x) = Knave ⇒ ¬S(x)
def knaves_tell_lies():
    """
    Encodes 'Knaves always tell lies'.

    In other terms: for all persons, being a knave implies lying.

    Returns
    -------
    Formula
   
    """
    # TASK 1
    # Your code here
    # Don't forget the return statement!
    x = Const('x', Person)
    return ForAll([x], Implies(R(x) == Knave, Not(S(x))))

# Now, we can set up specific puzzles by encoding them. For instance
# A: "B is the spy!"
# B: "No, C is the spy!"
# C: "B lies! B is definitely the spy!
def puzzle_example():
    """
    Encodes the claims in the following puzzle:
    
    A: "B is the spy!"
    B: "No, C is the spy!"
    C: "B lies! B is definitely the spy!

    Returns
    -------
    dict : Person : formula
       The claim made by each person.
    """
    # Here the dictionary key is who speaks, and the value is the encoding of what they say.
    return {A : R(B) == Spy, # B is the spy!
            B : And(S(A) == False, R(C) == Spy), # No [A lies], C is the spy!
            C : And(S(B) == False, R(B) == Spy)} # No [B lies], B is the spy!


def puzzle_task():
    """
    Encodes the claims in the following puzzle:

    A: "I am the Knight."
    B: "A speaks the truth!"
    C: "I am the spy."

    Returns
    -------
    dict : Person : formula
       The claim made by each person.
    """
    # TASK 2: Encode the puzzle described in the docstring above.
    # Look at puzzle_example above for an idea of how to do it.
    # return # YOUR CODE HERE
    return {A : R(B) == Knight,
            B : S(A) == True,
            C : R(C) == Spy}

# However, we can't just add the claims as constraints 
# - they may not be true!
# Instead we need to encode that they are true if and only if
# the person speaking is a Knight or possibly a Spy telling the truth!
def encode_statements(claims):
    """
    Encodes that a statement is true only if it is told by a knight,
    or by a spy who tells the truth.

    Parameters
    ----------
    claims : dict {Person : formula}

    Returns
    formula (conjunction of statements).
    """
    return And([claims[x] == Or(R(x) == Knight, And(R(x) == Spy, S(x))) for x in claims])

def resultstring(m):
    """
    Evaluates R,S for A,B,C and makes a result string.

    Parameters
    ----------
    m : z3 model

    Returns
    -------
    str
       Roles and truth for each person.
    """
    return "\n".join(f"{p} is a {m.evaluate(R(p))} and told a {'truth' if m.evaluate(S(p)) else 'lie'}"
                     for p in (A,B,C))

if __name__ == "__main__":
    # Get the general constraints
    d1 = abc_different() # Alt: `d1 = all_persons_have_different_roles()`
    d2 = knights_tell_truths()
    d3 = knaves_tell_lies()
    
    print("--------------")
    # Now we can solve some puzzles:
    print("Example puzzle")
    print("--------------")
    # Hack: extract the puzzle from the docstring and print it.
    print("\n".join(puzzle_example.__doc__.split('\n')[3:6]))
    # Get the puzzle
    print("solution:")
    claims = puzzle_example()
    statements = encode_statements(claims)
    # Solve the puzzle.
    s = Solver() # This creates an z3 solver object
    s.add(d1,d2,d3,statements) # Add constraints and statements.
    if s.check() == sat: # Must always check that a solution exists.
        m = s.model() # Get the model.
        print(resultstring(m)) # Format the answer and print it.
    else:
        print("Puzzle unsatisfiable.")

    # Now we can solve some puzzles:
    print("-----------")
    print("Task puzzle")
    print("-----------")
    # Hack: extract the puzzle from the docstring and print it.
    print("\n".join(puzzle_task.__doc__.split('\n')[3:6]))
    print("solution:")
    # Get the puzzle
    claims = puzzle_task()
    statements = encode_statements(claims)
    # Solve the puzzle.
    s = Solver()
    s.add(d1,d2,d3,statements) # Add constraints and statements.
    if s.check() == sat:
        m = s.model()
        print(resultstring(m))
    else:
        print("Puzzle unsatisfiable.")



