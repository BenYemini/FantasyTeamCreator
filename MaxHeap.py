from Player import *


class MaxHeap:
    # initializing the constructor.
    def __init__(self):
        # Initializing the heap with no elements in it
        self._heap = []
        self.size = 0

    # push is used to insert new player to the heap.
    def push(self, player):
        # Appending the player given by user at the last
        self._heap.append(player)
        self.size += 1  # Adding 1 to the size counter
        # Calling the bottom_up() to ensure heap is in order.
        _bottom_up(self._heap, self.size - 1)

    def delete_max(self):
        if self.size == 1:
            self._heap.pop()
            return
        else:
            _swap(self._heap, self.size - 1, 0)
            self._heap.pop()
            self.size -= 1

            # Calling the top_down function to ensure that the heap is still in order
            _top_down(self._heap, 0)

    # Returns the first element (The root).
    def peek(self) -> Player:
        return self._heap[0]

    # Returns the number of players in the heap.
    def get_size(self):
        return self.size

    # Prints the players in the heap
    def print(self):
        for player in self._heap:
            print(player.print())


# Swaps value in heap between i and j index
def _swap(L, i, j):
    L[i], L[j] = L[j], L[i]


# This is a private function used for traversing up the tree and ensuring that heap is in order
def _bottom_up(heap, index):
    # Finding the root of the element
    root_index = (index - 1) // 2

    # If we are already at the root node return nothing
    if root_index < 0:
        return

    # If the current Player has greater total grade than the root node, swap them
    if heap[index].get_total_grade() > heap[root_index].get_total_grade():
        _swap(heap, index, root_index)
        # Again call bottom_up to ensure the heap is in order
        _bottom_up(heap, root_index)


# This is a private function which ensures heap is in order after root is popped
def _top_down(heap, index):
    child_index = 2 * index + 1
    # If we are at the end of the heap, return nothing
    if child_index >= len(heap):
        return

    # For two children swap with the one who has greater total grade.
    if child_index + 1 < len(heap) and \
            heap[child_index].get_total_grade() < heap[child_index + 1].get_total_grade():
        child_index += 1

    # If the child has a smaller total grade than the current Player, swap them
    if heap[child_index].get_total_grade() > heap[index].get_total_grade():
        _swap(heap, child_index, index)
        _top_down(heap, child_index)
