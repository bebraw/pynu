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
from facade import ConnectionsFacade
from node import Node


class ParentFacade(ConnectionsFacade):

    def append(self, *items):
        raise AttributeError


class TreeNode(Node):
    _types = {'children': 'parent', }
    _facades = {'parent': ParentFacade, }

    def root(self):
        """Finds the root node.

        >>> node1, node2a, node2b = TreeNode(), TreeNode(), TreeNode()
        >>> node3a, node3b = TreeNode(), TreeNode()
        >>>
        >>> node1.children = (node2a, node2b)
        >>> node2a.children = (node3a, node3b)
        >>>
        >>> assert node1.root() == node1
        >>> assert node2a.root() == node1
        >>> assert node2b.root() == node1
        >>> assert node3a.root() == node1
        """
        if self.parent:
            return self.parent('parent=None')

        return self

    def walk(self):
        """Walks through the nodes beginning from the current one in preorder.

        >>> node1, node2a, node2b = TreeNode(), TreeNode(), TreeNode()
        >>> node3a, node3b = TreeNode(), TreeNode()
        >>>
        >>> node1.children = (node2a, node2b)
        >>> node2a.children = (node3a, node3b)
        >>> result = (node1, node3a, node3b, node2a, node2b)
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
