from wilt_amaze_slack_node import Node, exceptions
import unittest


class TestNodeTree(unittest.TestCase):
    def setUp(self) -> None:
        self.tree = Node(data="a")

        self.stem1 = Node("b")
        self.leaf1 = Node("c")
        self.leaf2 = Node("d")
        self.stem1.insert(self.leaf1)
        self.stem1.insert(self.leaf2)

        self.stem2 = Node("e")
        self.leaf3 = Node("f")
        self.leaf4 = Node("g")
        self.stem2.insert(self.leaf3)
        self.stem2.insert(self.leaf4)

        self.tree.insert(self.stem1)
        self.tree.insert(self.stem2)

        return super().setUp()

    def test_tree_has_leaf(self):
        self.assertTrue(self.tree.has_descendant(self.leaf4))

    def test_tree_has_self_as_descendant(self):
        self.assertTrue(self.tree.has_descendant(self.tree))

    def test_tree_does_not_have_orphan(self):
        self.assertFalse(self.tree.has_child(Node("h")))

    def test_cannot_insert_int(self):
        with self.assertRaises(TypeError):
            self.tree.insert(0)

    def test_cannot_insert_str(self):
        with self.assertRaises(TypeError):
            self.tree.insert("")

    def test_cannot_insert_object(self):
        with self.assertRaises(TypeError):
            self.tree.insert(object)

    def test_cannot_insert_builtin_class(self):
        with self.assertRaises(TypeError):
            self.tree.insert(int)
    
    def test_leaf_is_descendant_of_self(self):
        self.assertTrue(self.leaf1.has_descendant(self.leaf1))

    def test_siblings_in_subtree(self):
        self.assertTrue(self.leaf1.is_sibling_of(self.leaf2))

    def test_not_siblings_nodes_in_different_subtrees(self):
        self.assertFalse(self.leaf1.is_sibling_of(self.leaf4))

    def test_not_siblings_parent_and_child(self):
        self.assertFalse(self.leaf1.is_sibling_of(self.stem1))

    def test_not_siblings_node_and_self(self):
        self.assertFalse(self.leaf1.is_sibling_of(self.leaf1))

class TestCircular(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Node('a')
        self.stem1 = Node('b')
        self.stem2 = Node('c')

        self.stem1.insert(self.stem2)
        self.root.insert(self.stem1)

        return super().setUp()

    def test_cannot_insert_self(self):
        with self.assertRaises(exceptions.CircularError):
            self.root.insert(self.root)
    
    def test_node_cannot_be_child_of_caller(self):
        with self.assertRaises(exceptions.CircularError):
            self.root.insert(self.root)

    def test_child_node_cannot_be_ancestor(self):
        with self.assertRaises(exceptions.CircularError):
            self.stem2.insert(self.root)

if __name__ == "__main__":
    unittest.main()
