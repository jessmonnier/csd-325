# Jess Monnier, Assignment 2.2, 11 December 2025
'''
This is an adaptation of a function found on codewars. The original is
commented out at the bottom of this script.

The purpose is to take a list and an integer (n) and return the list item
that would be left if you removed every nth item from the list, continuing
the count at the beginning if you reach the end of the list.

I thought this was an interesting solution, but refactored it to be more
readable and easier to step through with the debugger.
'''

# Import deque, used here for its rotate method
from collections import deque

# Define the function, requiring two variables as input
def josephus(arr, n):

    # The first variable is expected to be a list. Create a deque out of it.
    q = deque(arr)

    # We only want to iterate as many times as there are items in the list, so
    # even though we don't use each item, they work as a counter.
    for item in arr:

        # By subtracting n from 1, we ensure that the deque will rotate such that
        # the first n-1 items are moved to the end of the deque, meaning that the
        # nth item is now the first element.
        q.rotate(1-n)

        # Pop out that leftmost element and set recent to that value. The use of
        # pop actually removes the element from the list, so the deque will be
        # wittled down over the course of the iterations to a final "winning" element.
        recent = q.popleft()
    
    # After the loop, the final remaining item will be stored in recent, so return that
    return recent

# Set the values of the variables to feed into the function
arr = [1, 2, 3, 4, 5]
n = 4

# Print the result of the function.
print(josephus(arr, n))

# Original code from codewars by user falsetru for the Josephus Permutation kata:
'''
from collections import deque

def josephus(items,k):
    q = deque(items)
    return [[q.rotate(1-k), q.popleft()][1] for _ in items]
'''