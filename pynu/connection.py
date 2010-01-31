# -*- coding: utf-8 -*-
"""
Connection classes.
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

# TODO: test Connections directly!
class Connections(list):

    def __init__(self, owner, nodes=[]):
        self._owner = owner

        super(Connections, self).__init__(nodes)

    def __eq__(self, other):
        """Checks if connections are equal.

        >>> con1, con2 = Connections(), Connections()
        >>>
        >>> assert con1 == None
        >>>
        >>> con1.append('foo')
        >>> con2.append('foo')
        >>>
        >>> assert con1 == con2
        >>>
        >>> con2.append('bar')
        >>>
        >>> assert not con1 == con2
        """
        if len(self) == 0 and other is None:
            return True

        return super(Connections, self).__eq__(other)

    def ___neq__(self, other):
        """Checks if connections are not equal.

        >>> con1, con2 = Connections(), Connections()
        >>>
        >>> assert con1 == None
        >>>
        >>> con1.append('foo')
        >>> con2.append('foo')
        >>>
        >>> assert con1 == con2
        >>>
        >>> con2.append('bar')
        >>>
        >>> assert not con1 == con2
        """
        return not self == other

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
        for node in self:
            self.remove(node)

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
                super(Connections, self).append(item)

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
            if item in self._nodes[type]:
                self._nodes[type].remove(item)

    def find(self, connection_type, **rules):
        """Finds nodes matching to given rules. The idea is that the method
        seeks based on the type of the container. For example in case
        "node.parents.find" is invoked, it goes through all parents beginning
        from the parents of the given node.

        Default case

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

        Cyclic case

        >>> node1, node2 = Node(), Node()
        >>>
        >>> node1.children = node2
        >>> node2.children = node1
        >>>
        >>> node1.name = 'joe'
        >>> node2.name = 'jack'

        Single argument, single result

        >>> assert node1.children.find(name='joe') == node1
        >>> assert node1.children.find(name='jack') == node2
        """
        found_nodes = self._recursion(rules, [], [], connection_type)

        if len(found_nodes) > 0:
            return found_nodes[0] if len(found_nodes) == 1 else found_nodes

    def _recursion(self, rules, found_nodes, visited_nodes,
            connection_type):
        visited_nodes.append(self._owner)

        for node in self:
            try:
                if self._all_match(node, rules):
                    found_nodes.append(node)
            except AttributeError:
                pass

            if node not in visited_nodes:
                facade = getattr(node, connection_type)

                # XXX: utter nastiness. figure out a better way
                facade._connections[facade._connection_type.name]._recursion(
                    rules, found_nodes, visited_nodes, connection_type)

        return found_nodes

    def _all_match(self, node, rules):
        for wanted_attribute, wanted_value in rules.items():
            attribute_value = getattr(node, wanted_attribute)

            if isinstance(wanted_value, str):
                matched = re.match(wanted_value, attribute_value)
            else:
                matched = wanted_value == attribute_value

            if not matched:
                return False

        return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()
