# -*- coding: utf-8 -*-
"""
Helper classes.
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
import re

class Node(object):
    _children_name = 'children'
    _parents_name = 'parents'

    def __init__(self):
        def set_container(name, complementary_name):
            setattr(self, name, NodeContainer(self, name, complementary_name))

        set_container(self._children_name, self._parents_name)
        set_container(self._parents_name, self._children_name)

    def __setattr__(self, name, value):
        '''
        Assignment of children/parents resets previous content and creates
        needed links to nodes. Otherwise setting attributes works as expected.

        Simple assignment

        >>> node1, node2 = Node(), Node()
        >>> node1.children = node2
        >>>
        >>> assert node1.children[0] == node2
        >>> assert node2.parents[0] == node1

        Tuple assignment

        >>> node1, node2, node3 = Node(), Node(), Node()
        >>> node1.children = (node2, node3)
        >>>
        >>> assert node1.children[0] == node2
        >>> assert node2.parents[0] == node1
        >>> assert node1.children[1] == node3
        >>> assert node3.parents[0] == node1

        Assign value to an attribute
        
        >>> node = Node()
        >>>
        >>> node.value = 13
        >>> assert node.value == 13
        '''
        def container_template(container_name):
            if hasattr(self, container_name):
                container = getattr(self, container_name)

                container.empty()

                if hasattr(value, '__iter__'):
                    container.append(*value)
                else:
                    container.append(value)
            else:
                super(Node, self).__setattr__(name, value)

        if name in (self._children_name, self._parents_name):
            container_template(name)
        else:
            super(Node, self).__setattr__(name, value)


class NodeContainer(list):

    def __init__(self, owner, name, complementary_name):
        super(NodeContainer, self).__init__()
        self.owner = owner
        self.name = name
        self.complementary_name = complementary_name

    def empty(self):
        """Empties container content.

        >>> node1, node2 = Node(), Node()
        >>>
        >>> node1.children = node2
        >>> node1.children.empty()
        >>>
        >>> assert len(node1.children) == 0
        >>> assert len(node2.parents) == 0
        """
        for item in self:
            super(NodeContainer, self).remove(item)
            complementary_items = getattr(item,
                self.complementary_name)
            complementary_items.remove(self.owner)

    def append(self, *items):
        """Appends given items to container.

        Regular case
        
        >>> node1, node2 = Node(), Node()
        >>>
        >>> node1.children = node2
        >>>
        >>> assert node1.children[0] == node2
        >>> assert node2.parents[0] == node1

        Cycles are allowed by default

        >>> node1.parents.append(node2)
        >>>
        >>> assert node2.children[0] == node1
        >>> assert node1.parents[0] == node2

        Append multiple times

        >>> node1, node2 = Node(), Node()
        >>> node1.children.append(node2)
        >>> node1.children.append(node2)
        >>>
        >>> assert node1.children[0] == node2
        >>> assert node2.parents[0] == node1
        >>> assert len(node1.children) == 1
        >>> assert len(node2.parents) == 1

        Append multiple at once

        >>> node1, node2, node3 = Node(), Node(), Node()
        >>>
        >>> node1.children = (node2, node3)
        >>>
        >>> assert len(node1.children) == 2
        >>> assert node2 in node1.children
        >>> assert node3 in node1.children
        """
        for item in items:
            if item not in self:
                super(NodeContainer, self).append(item)
                complementary_items = getattr(item,
                    self.complementary_name)
                complementary_items.append(self.owner)

    def remove(self, *items):
        """Removes given items from container.

        Regular case

        >>> node1, node2 = Node(), Node()
        >>>
        >>> node1.children = node2
        >>> node1.children.remove(node2)
        >>>
        >>> assert len(node1.children) == 0
        >>> assert len(node2.parents) == 0

        Remove multiple times

        >>> node1, node2 = Node(), Node()
        >>>
        >>> node1.parents = node2
        >>> node1.parents.remove(node2)
        >>> node1.parents.remove(node2)
        >>> node1.parents.remove(node2)
        >>>
        >>> assert len(node1.parents) == 0
        >>> assert len(node2.children) == 0

        Remove multiple at once

        >>> node1, node2, node3 = Node(), Node(), Node()
        >>>
        >>> node1.children = (node2, node3)
        >>> node1.children.remove(node2, node3)
        >>>
        >>> assert len(node1.children) == 0
        """
        for item in items:
            if item in self:
                super(NodeContainer, self).remove(item)
                complementary_items = getattr(item,
                    self.complementary_name)
                complementary_items.remove(self.owner)

    def find(self, **kvargs):
        """Finds child nodes matching to given rules.

        >>> node1, node2, node3, node4 = Node(), Node(), Node(), Node()
        >>>
        >>> node1.children = (node2, node3)
        >>> node3.parents.append(node4)
        >>>
        >>> node1.name = 'joe'
        >>> node1.value = 13
        >>> node2.color = 'blue'
        >>> node3.color = 'black'
        >>> node4.value = 13

        Single argument, single result

        >>> assert node2.parents.find(name='joe') == node1
        >>> assert node1.children.find(color='blue') == node2

        Single argument, multiple results

        >>> assert node3.parents.find(value=13) == [node1, node4]

        Multiple arguments, single result

        >>> assert node2.parents.find(name='joe', value=13) == node1

        Regex argument (match anything except newline)

        >>> assert node2.parents.find(name='.') == node1

        Regex argument (match from beginning)

        >>> assert node1.children.find(color='^bl') == [node2, node3]

        No result

        >>> assert node2.parents.find(color='red') == None
        """
        found_nodes = self._recursion(kvargs, [], [])
        
        if len(found_nodes) > 0:
            return found_nodes[0] if len(found_nodes) == 1 else found_nodes

    def _recursion(self, search_clauses, found_nodes, visited_nodes):
        visited_nodes.append(self.owner)

        for node in self:
            try:
                all_match = True
                for wanted_attribute, wanted_value in search_clauses.items():
                    attribute_value = getattr(node, wanted_attribute)

                    if isinstance(wanted_value, str):
                        matched = re.match(wanted_value, attribute_value)
                    else:
                        matched = wanted_value == attribute_value

                    if not matched:
                        all_match = False
                        break

                if all_match:
                    found_nodes.append(node)
            except AttributeError:
                pass

            if node not in visited_nodes:
                node_container = getattr(node, self.name)

                node_container._recursion(search_clauses, found_nodes,
                    visited_nodes)

        return found_nodes
