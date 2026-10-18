from __future__ import annotations

import threading

class Node:

    # Initially each node knows the location of the next
    # node in the doubled linked list
    def __init__(self, data):
        self.data = data
        self.next: Node | None = None
        self.previous: Node | None = None

class DoubleLinkedList:
    def __init__(self, max_size=None):
        self.head: Node | None = None  # first node; None if empty
        self.tail: Node | None = None  # last node; None if empty
        self.size = 0
        self.max_size = max_size  
        self.lock = threading.Lock()

    def append(self, data):
        # Validate input data
        if isinstance(data, str) and len(data) > 1000:  
            raise ValueError("Data size exceeds maximum limit")

        with self.lock:
            if self.max_size is not None and self.size >= self.max_size:
                raise ValueError("Double linked list is full")

            new_node = Node(data)
            if self.tail is None:
                # Empty list: the new node is both first and last.
                self.head = new_node
                self.tail = new_node
                new_node.previous = None
            else:
                # Link the old last node to the new one, then move tail forward.
                new_node.previous = self.tail
                self.tail.next = new_node
                self.tail = new_node
            self.size += 1
            
    def remove(self) -> Node:
        """Remove the last node data. Raises ValueError if the doubled linked list is empty."""
        with self.lock:
            if self.tail is None:
                raise ValueError("Double linked list is empty")

            removed = self.tail
            self.tail = removed.previous
            if self.tail is None:
                self.head = None
            else:
                self.tail.next = None
            self.size -= 1
            return removed.data

    def print_list(self):
        with self.lock:
            current = self.head
            while current:
                print(current.data, end=" ")
                current = current.next

    def print_list_reverse(self):
        with self.lock:
            if self.tail is None:
                print("Double linked list is empty")
            else:
                current = self.tail
                while current:
                    print(current.data, end=" ")
                    current = current.previous


if __name__ == "__main__":
    # Test 1 - Append Multiple Data Types
    print("First test:" ,end="\n")
    linked_list = DoubleLinkedList()
    linked_list.append("A")
    linked_list.append(1)
    linked_list.append(0.1)
    linked_list.print_list()
    print("\n")

    # Test 2 - Print the Linked List in Reverse
    print("Second test:" ,end="\n")
    linked_list = DoubleLinkedList()
    linked_list.append("A")
    linked_list.append("B")
    linked_list.append(10)
    linked_list.append(20)
    linked_list.print_list_reverse()
    print("\n")

    # Test 3 - Remove last node, then print reverse
    print("Third test:", end="\n")
    linked_list = DoubleLinkedList()
    linked_list.append("A")
    linked_list.append("B")
    linked_list.append(10)
    linked_list.append(20)
    removed = linked_list.remove()
    print("Removed:", removed)
    linked_list.print_list_reverse()
    print("\n")
    linked_list.remove()
    linked_list.remove()
    linked_list.remove()
    linked_list.print_list_reverse()
    print("\n")