# -*- coding: utf-8 -*-
"""
Tree utilities.
"""
"""
Pynu - Python Node Utilities
Copyright (C) 2010 Juho Vepsäläinen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/
"""
from node import Node

# parent = file.parent
# parent.find (find in container)
# parent.children (children in node) -> add property for this
# -> general problem! applies for children too (needs parents property)

# parent.parent.parent -> ok!
# parents.parents.parents -> ok! (each step accumulates!)
# -> container(container(container()))
# what about parents.children.parents? -> ok

# test remove with chaining!

# test behavior of remove with chaining!

class TreeNode(Node):
    _types = {'children': 'parent', }

    def find_root(self):
        """Finds the root node.

        Regular case

        >>> node1, node1a = TreeNode(), TreeNode()
        >>> node1b, node1a1 = TreeNode(), TreeNode()
        >>> node1.children.append(node1a, node1b)
        >>> node1a.children.append(node1a1)
        >>>
        >>> assert node1.find_root() == node1
        >>> assert node1a.find_root() == node1
        >>> assert node1b.find_root() == node1
        >>> assert node1a1.find_root() == node1
        """
        if self.parent:
            return self.parent.find(parent=None)

        return self

    def walk(self):
        """Walks through the nodes beginning from the current one in preorder.

        >>> node1, node2, node3 = TreeNode(), TreeNode(), TreeNode()
        >>> node4, node5 = TreeNode(), TreeNode()
        >>>
        >>> node1.children = (node2, node5)
        >>> node2.children = (node3, node4)
        >>> result = (node1, node3, node4, node2, node5 )
        >>>
        >>> for i, node in enumerate(node1.walk()):
        ...    assert node == result[i], '%s %s %s' % (i, node, result[i])
        """

        def _walk(nodes):
            for node in nodes:
                for child in _walk(node.children):
                    yield child

                yield node

        yield self

        for child_walk_node in _walk(self.children):
            yield child_walk_node

if __name__ == "__main__":
    import doctest
    doctest.testmod()
