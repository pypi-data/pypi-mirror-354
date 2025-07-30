# from __future__ import annotations
from typing import Optional, Self, Any
from dataclasses import dataclass, field

from wilt_amaze_slack_node import exceptions

# T = TypeVar("T", bound="Node")


@dataclass(init=True)
class Node[T: "Node"]:
    """
    :param data: any Any data to store in the node

    Initialize a tree by creating a root node and using the `insert` method to add stems and leafs
    ```python
    root = Node('a')
    stem = Node('b')
    leaf1 = Node('c')
    leaf2 = Node('d')

    stem1.insert(leaf1)
    stem1.insert(leaf2)
    root.insert(stem)
    ```
    """

    data: Optional[Any] = field(init=True, default=None)
    """Arbitrary data stored in the node"""

    parent: Optional[T] = field(init=False)
    """The immediate predecessor in the tree. `None` if node is the tree root"""

    children: list[T] = field(init=False, default_factory=list)
    """Immediate children of the node"""

    def get_root(self) -> T | Self:
        """:returns: T | Self"""
        if not self.parent:
            return self

        root = None
        next_parent = self.parent
        while not root:
            current_node = next_parent
            if current_node.parent:
                next_parent = current_node.parent
            else:
                root = current_node

        return root

    def has_descendant(self, node: T) -> bool:
        """Searches entire subtree for the given node
        :param node: T The node instance to search for
        """
        if self == node:
            return True

        def search_descendants(children: list[T], node: T) -> bool | None:
            """Search for a node with the the pre-order traversal algorithm
            https://en.wikipedia.org/wiki/Tree_traversal#Pre-order_implementation

            :param children: list[T]
            :param node: T
            """

            for child in children:
                if child == node:
                    return True
                if not child.is_leaf:
                    if search_descendants(child.children, node):
                        return True

        return search_descendants(self.children, node) or False

    def has_child(self, node: T) -> bool:
        """Determine if the provided node is an immediate child of this node
        :param node: T The node instance to search for
        """
        for child in self.children:
            if child == node:
                return True
        return False

    def has_ancestor(self, node: T) -> bool:
        """Determine if the provided node is an ancestor of this node
        :param node: T The node instance to search for
        """

        def search_parent(current_node: T | Self, node: T) -> bool:
            next_parent = (
                current_node.parent if hasattr(current_node, "parent") else None
            )
            if next_parent:
                if next_parent == node:
                    return True
                return search_parent(next_parent, node)
            return False

        return search_parent(self, node)

    def is_sibling_of(self, node:T)->bool:
        """`True` if caller and node share a parent
        :param node: T
        """
        # Always false if:
        # - either node is root
        # - self is node 
        if self == node or self.is_root or node.is_root:
            return False

        return self.parent == node.parent

    @property
    def is_leaf(self) -> bool:
        """`True` if the node has no children"""
        return len(self.children) == 0

    @property
    def is_root(self)->bool:
        """`True` if node has no parent"""
        return not hasattr(self, "parent")

    def insert(self, node: T, deracinate=False) -> None:
        """Insert a child node

        :param node: Node The node to insert as a child of the calling node.
        :param deracinate: bool If node already has a parent, overwrite the parent property.
        :raises: CircularError
        Restrictions:

            1. A node cannot be a child of itself
            2. A node cannot be a parent to an ancestor node
            3. A node cannot have two parents
            4. Cannot insert the same node twice
            5. A node cannot be an ancestor to a sibling
        """
        if not isinstance(node, type(self)):
            raise TypeError

        if self == node:
            raise exceptions.CircularError()

        # Node cannot already be a descendant
        if self.has_descendant(node):  # type: ignore
            raise exceptions.CircularError()

        # Node cannot be an ancestor
        if self.has_ancestor(node):  # type: ignore
            raise exceptions.CircularError()

        if hasattr(node, "parent") and node.parent is not None:
            if not deracinate:
                raise exceptions.InsertError(
                    message="Cannot overwrite parent on node: `deracinate` is `False`"
                )

        node.parent = self  # type: ignore
        self.children.append(node)  # type: ignore
