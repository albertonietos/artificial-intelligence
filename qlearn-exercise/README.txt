Implement q-learning
--------------------

In this exercise you will implement an algorithm which, given a Markov Decision Process, iteratively performs q-learning.

The q-learning is applied to the same 2D grid process as was used for the previous value iteration exercise.

Instructions
^^^^^^^^^^^^
1. To prepare for the exercise, read about q-learning.
2. Copy `template-qlearn.py` to `qlearn.py`
3. Read and understand all the code.
4. Implement the tasks

Tasks
^^^^^
There are four tasks in `qlearn.py`:
   - TASK 1: Implement the function `value_best_action`
   - TASK 2: Implement the function `execute`
   - TASK 3: Implement the function `q_learning`
   - TASK 4: Implement the function `make_policy`

Testing
^^^^^^^
- `python qlearn.py` :: Will execute a basic example.
- `python test_qlearn.py` :: Will execute a few unit tests.

Notes
^^^^^
- Your tasks involve picking things at random. The python `random` module is imported, and you may find some useful functions there (https://docs.python.org/3.7/library/random.html)
- When picking *actions* ("some action", in the words of the algorithm in section 8.2) the easiest is to do it uniformly at random. If you are interested, you could also implement some scheme that prefers better actions, e.g. based on Multi-arm Bandit problems, but this is optional.
- When picking successor states, note that the probability to select a particular successor state must match that in the MDP.

Good luck!

