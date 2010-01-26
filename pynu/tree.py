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

class TreeNode(Node):
    _parents_name = '_parents'

    def __setattr__(self, name, value):
        if name == 'parent':
            self._set_parent(value)
        else:
            super(TreeNode, self).__setattr__(name, value)

    @property
    def parent(self):
        """Gets the value of parent node.

        >>> node1, node2 = TreeNode(), TreeNode()

        No parent has been set yet
        
        >>> assert node1.parent is None

        Set parent

        >>> node1.parent = node2
        >>> assert node1.parent == node2
        """
        if len(self._parents) > 0:
            return self._parents[0]

    def _set_parent(self, value):
        """Sets the value of parent node. The parent has to be a TreeNode.

        >>> node1, node2, node3 = TreeNode(), TreeNode(), TreeNode()
        >>> node1.parent = node2
        >>> node1.parent = node3
        >>> assert node2.children == []
        >>> assert node3.children == [node1, ]
        """
        assert len(self._parents) <= 1
        assert isinstance(value, TreeNode)

        if len(self._parents) == 1:
            self._parents.remove(self._parents[0])

        value.children.append(self)

    def find_root(self):
        """Finds the root node.

        Regular case
        
        >>> node1, node1a = TreeNode(), TreeNode()
        >>> node1b, node1a1 = TreeNode(), TreeNode()
        >>> node1.children.append(node1a, node1b)
        >>> node1a.children.append(node1a1)
        >>> assert node1.find_root() == node1
        >>> assert node1a.find_root() == node1
        >>> assert node1b.find_root() == node1
        >>> assert node1a1.find_root() == node1

        Cyclic case

        >>> node1, node2 = TreeNode(), TreeNode()
        >>> node1.children.append(node2)
        >>> node2.children.append(node1)
        >>> assert node1.find_root() == None
        >>> assert node2.find_root() == None
        """
        node = self.parent

        if node is None:
            return self

        checked_nodes = set()
        while node.parent:
            node = node.parent

            if node in checked_nodes:
                return
            
            checked_nodes.add(node)

        return node

    def walk(self):
        """Walks through the nodes beginning from the current one in preorder.

        >>> node1, node2, node3 = TreeNode(), TreeNode(), TreeNode()
        >>> node4, node5 = TreeNode(), TreeNode()
        >>> node1.children = (node2, node5)
        >>> node2.children = (node3, node4)
        >>> result = (node1, node3, node4, node2, node5 )
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
