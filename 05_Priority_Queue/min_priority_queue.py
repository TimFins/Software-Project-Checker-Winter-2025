# min priority queue
#
# Software for educational purposes only. No warranty of any kind.
#
# Author: Jens Liebehenschel
# Copyright 2025


"""PLEASE NOTE!

This implementation uses an array to represent the priority queue to reduce complexity.
This is theoretically allowed, since a heap can safely be represented as an array, while a regular binary tree cannot.

You will use a tree data structure instead, therefore while these funtions left_child(), right_child() and parent() operate on array indices,
you will use methods from the PriorityQueue class, which implements them as a real tree.
"""


class MinPriorityQueue:
    MAX_SIZE = 10

    def __init__(self):
        self.heapsize = 0  # empty priority queue
        self.heap = [-1]*self.MAX_SIZE

    def is_empty(self):
        return self.heapsize <= 0

    def is_full(self):
        return self.heapsize >= self.MAX_SIZE

    def left_child(self, i):
        return 2*i + 1

    def right_child(self, i):
        return 2*i + 2

    def parent(self, i):
        return (i-1)//2

    def print(self):
        print(self.heap[0:self.heapsize])


def extract_min(pq):
    if not pq.is_empty():
        min_elem = pq.heap[0]
        pq.heapsize -= 1
        pq.heap[0] = pq.heap[pq.heapsize]
        heapify(pq, 0)
        return min_elem
    else:
        return False


def heapify(pq, i):
    if pq.left_child(i) < pq.heapsize and pq.heap[pq.left_child(i)] < pq.heap[i]:
        minimum = pq.left_child(i)
    else:
        minimum = i
    if pq.right_child(i) < pq.heapsize and pq.heap[pq.right_child(i)] < pq.heap[minimum]:
        minimum = pq.right_child(i)
    if minimum != i:
        pq.heap[i], pq.heap[minimum] = pq.heap[minimum], pq.heap[i]
        heapify(pq, minimum)


def insert(pq, elem):
    if not pq.is_full():
        pq.heap[pq.heapsize] = elem
        i = pq.heapsize
        while (i > 0) and pq.heap[i] < pq.heap[pq.parent(i)]:
            pq.heap[i], pq.heap[pq.parent(
                i)] = pq.heap[pq.parent(i)], pq.heap[i]
            i = pq.parent(i)
        pq.heapsize += 1
        return True
    else:
        return False


# Lower value = "more important" (higher up in the priority queue)
def increase_priority(pq, i, prio):
    if i >= 0 and i < pq.heapsize and prio < pq.heap[i]:
        pq.heap[i] = prio
        while (i > 0) and pq.heap[i] < pq.heap[pq.parent(i)]:
            pq.heap[i], pq.heap[pq.parent(
                i)] = pq.heap[pq.parent(i)], pq.heap[i]
            i = pq.parent(i)
        return True
    else:
        return False
