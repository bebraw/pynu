# -*- coding: utf-8 -*-
"""
Tree utilities.
"""
"""
Pynu - Python Node Utilities
Copyright (c) 2014 Juho Vepsäläinen

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from node import Node, NodeContainer


class ParentContainer(NodeContainer):

    def _set_content(self, content):
        """Sets content of the container. Note that the new content has to be
        a TreeNode.

        >>> node1, node2 = TreeNode(), TreeNode()
        >>> node2.parent._set_content(node1)
        >>>
        >>> assert node1.children == [node2, ]
        >>> assert node2.parent == [node1, ]
        >>>
        >>> node3 = TreeNode()
        >>> node2.parent._set_content(node3)
        >>>
        >>> assert node1.children == None
        >>> assert node2.parent == [node3, ]
        >>> assert node3.children == [node2, ]
        """
        assert isinstance(content, TreeNode)

        self.empty()
        self.append(content)


class TreeNode(Node):
    _parents_container = ParentContainer
    _parents_name = 'parent'

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
