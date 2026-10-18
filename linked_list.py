from __future__ import annotations

import threading
from collections.abc import Sized


class Node:
    """One element in the list: a value and a link to the next node."""

    def __init__(self, data: object) -> None:
        self.data = data
        self.next: Node | None = None  # None means this is the last node


class LinkedList:
    """Singly linked list with O(1) append via a tail pointer.

    Optional max_size caps how many nodes can be stored.
    Mutations and traversal share a lock so concurrent use is safe.
    """

    def __init__(self, max_size: int | None = None) -> None:
        self.head: Node | None = None  # first node; None if empty
        self.tail: Node | None = None  # last node; None if empty
        self.size: int = 0
        self.max_size = max_size
        self.lock = threading.Lock()

    def append(self, data: Sized) -> None:
        """Add a node at the end of the list."""
        if len(data) > 1000:
            raise ValueError("Data size exceeds maximum limit")

        with self.lock:
            if self.max_size is not None and self.size >= self.max_size:
                raise ValueError("Linked list is full")

            new_node = Node(data)
            if self.tail is None:
                # Empty list: the new node is both first and last.
                self.head = new_node
                self.tail = new_node
            else:
                # Link the old last node to the new one, then move tail forward.
                self.tail.next = new_node
                self.tail = new_node
            self.size += 1

    def remove(self) -> None:
        """Remove the last node. Raises ValueError if the list is empty."""
        with self.lock:
            if self.head is None:
                raise ValueError("Linked list is empty")

            if self.head.next is None:
                # Only one node: list becomes empty.
                self.head = None
                self.tail = None
            else:
                # Find the node *before* the tail so we can unlink the last node.
                current = self.head
                while current.next is not None and current.next.next is not None:
                    current = current.next
                current.next = None
                self.tail = current
            self.size -= 1

    def print_list(self) -> None:
        """Print all values from head to tail, separated by spaces."""
        with self.lock:
            current = self.head
            while current:
                print(current.data, end=" ")
                current = current.next


# Example usage
ll = LinkedList(max_size=1000)
try:
    print("\nStart adding:")
    ll.append("Data 1")
    ll.append("Data 2")
    ll.append("Data 3")
    ll.append("Data 4")
    ll.print_list()
    print("\nStart removing")
    ll.remove()
    ll.remove()
    ll.remove()
    ll.remove()
    ll.remove()  # list is already empty; caught below
    ll.print_list()
except ValueError as e:
    print(e)
