
Programming Exercise 1: Knight, Knave, Spy
------------------------------------------

This exercise is about solving a version of a classic logic puzzle about telling truth from lying.
There are lots of puzzles like this, most of them easily expressible in logic. Some of the most famous ones are the Knights and Knaves puzzles presented in some of the books by Raymond Smullyan.

The puzzles usually start like this

    You are travelling on the island of Knights and Knaves, bound for its capital city, and have just come upon a fork in the road. Two old men sit silently on a bench under a tree. Not knowing which way to go (and, because this is the twenty-first century, not having phone reception) you decide to ask for directions.
    The problem is that one of them is a Knight - who always tells the truth, while the other one is a Knave - who always lies. But, you don't know who is the Knight and who is the Knave!

Usually this introduction is followed by some statements from the persons, and it is up to you to figure out who tells the truth and who lies.

In our version, we have three persons, boringly called A,B, and C, and three different roles:

- Knights : always tell truth
- Knaves  : always lies
- Spies   : who sometimes lies and sometimes tell the truth

You know that there is always one spy, one knave, and one knight.

In the puzzles, some persons say something, and we do not know whether they are knights, knaves or spies, and hence we have to *infer* what the persons are and whether they are lying or telling the truth.


For example:

    A: "B is the spy!"
    B: "No, C is the spy!"
    C: "B lies! B is definitely the spy!

(Solution can be found in the end of the file.)

This exercise is about solving such puzzles and encoding the statements the three persons made. It is a tutorial for using quantifiers (the `ForAll` statement), domains, and functions in z3. 


Instructions
^^^^^^^^^^^^

1. Copy the file `template-knightsknaves.py` to `knightsknaves.py`
2. Read and understand the code. It is formulated as a kind of tutorial with a lot of comments explaining how the puzzle is encoded.
3. Implement TASK 1 - encoding that Knaves lies.
4. Implement TASK 2 - encoding of a specific puzzle.

Testing
^^^^^^^
1. `python test_knightsknaves.py` : Will run a set of unit tests. Note that these are not exhaustive (not to give away the solution to the exercise). They will however catch some basic mistakes.
2. `python knightsknaves.py` : This will print the solution to both the example puzzle and the puzzle of TASK 2. You can get an idea of if your encoding is correct by checking if the solution the program prints is compatible with the puzzle (remember checking is easy, finding an answer, not always so).

Good luck!










(Solution to example: A is a Knave, B is a Knight, C is a spy (and lies))
