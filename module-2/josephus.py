from collections import deque

def josephus(arr, n):
    q = deque(arr)
    for item in arr:
        q.rotate(1-n)
        recent = q.popleft()
    return recent

arr = [1, 2, 3, 4, 5]
n = 4

print(josephus(arr, n))

# Original code from codewars by user falsetru for the Josephus Permutation kata:
'''
from collections import deque

def josephus(items,k):
    q = deque(items)
    return [[q.rotate(1-k), q.popleft()][1] for _ in items]
'''