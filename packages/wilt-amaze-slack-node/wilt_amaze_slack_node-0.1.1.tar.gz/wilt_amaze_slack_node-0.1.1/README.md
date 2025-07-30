# Overview
Data primitive for tree-shaped data structures

# Usage
```python
import Node from tree

root = Node('a')
subtree = Node('b')
leaf1 = Node('c')
leaf2 = Node('d')
leaf3 = Node('e')
subtree.insert(leaf1)
subtree.insert(leaf2)
subtree.insert(leaf3)

root.insert(subtree)

print(root.has_descendant(leaf3))
# True
```
