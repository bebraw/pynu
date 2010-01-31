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


# TODO: add support for custom attrs at append? -> node1.children.append(node2,
# weight=0.5) -> adds new child for node1. connection has 0.5 as weight
# how to adjust/access connection attrs? <get connection>.<attr>


# TODO: test Connections directly!
class Connections(list):

    def __init__(self, nodes=[]):
        super(Connections, self).__init__(nodes)

    def __eq__(self, other):
        """Checks if container contents are equal to other.

        >>> node1, node2, node3 = Node(), Node(), Node()
        >>>
        >>> assert node1.children == None
        >>>
        >>> node1.children = node3
        >>> node2.children = node3
        >>>
        >>> assert node1.children == [node3, ]
        >>> assert node1.children == node2.children
        """
        if len(self) == 0 and other is None:
            return True

        return self == other

    def ___neq__(self, other):
        """Checks if container contents are not equal to other.

        >>> node1, node2, node3 = Node(), Node(), Node()
        >>>
        >>> node1.children = node3
        >>> node2.children = node3
        >>>
        >>> assert node1.children != [node2, ]
        >>> assert node1.children != node3.children
        """
        return not self == other

    def _set_content(self, content):
        """Sets content of the container.

        >>> node1, node2 = Node(), Node()
        >>> node1.children._set_content(node2)
        >>>
        >>> assert node1.children == [node2, ]
        >>> assert node2.parents == [node1, ]
        >>>
        >>> node3 = Node()
        >>> node1.children._set_content(node3)
        >>>
        >>> assert node1.children == [node3, ]
        >>> assert node2.parents == None
        """
        self.empty()

        if hasattr(content, '__iter__'):
            self.append(*content)
        else:
            self.append(content)

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

    def find(self, **rules):
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
        found_nodes = self._recursion(rules, [], [])

        if len(found_nodes) > 0:
            return found_nodes[0] if len(found_nodes) == 1 else found_nodes

    def _recursion(self, search_clauses, found_nodes, visited_nodes):
        #visited_nodes.append(self.owner) (no ref to owner anymore) # XXX
        return None

        for node in self:
            try:
                if self._all_match(node, search_clauses):
                    found_nodes.append(node)
            except AttributeError:
                pass

            if node not in visited_nodes:
                node_container = getattr(node, self.name)

                node_container._recursion(search_clauses, found_nodes,
                    visited_nodes)

        return found_nodes

    def _all_match(self, node, search_clauses):
        for wanted_attribute, wanted_value in search_clauses.items():
            attribute_value = getattr(node, wanted_attribute)

            if isinstance(wanted_value, str):
                matched = re.match(wanted_value, attribute_value)
            else:
                matched = wanted_value == attribute_value

            if not matched:
                return False

        return True


class AccumulatorFacade(object):

    def __init__(self, type_manager, nodes):
        assert isinstance(nodes, list)
        self._type_manager = type_manager
        self._nodes = Connections(nodes)

    def __len__(self):
        return len(self._nodes)

    def __eq__(self, other):
        return self._nodes == other

    def __neq__(self, other):
        return self._nodes != other

    def __getitem__(self, index):
        return self._nodes[index]

    def __getattr__(self, name):
        type = self._type_manager.get_type(name)

        if type:
            nodes = list()

            for node in self._nodes:
                nodes.append(getattr(node, type))

            return AccumulatorFacade(self._type_manager, nodes, type)

    def __setattr__(self, name, value):
        if '_nodes' in self.__dict__:
            for node in self._nodes:
                setattr(node, name, value)
        else:
            super(AccumulatorFacade, self).__setattr__(name, value)

    def find(self, **rules):
        self._nodes.find(**rules)

# handle accum set (ie. node.parents.parents.color = 'blue' should set color of
# all belonging to that selection)
# handle node.parents.parents.find(color='blue')
class ConnectionsFacade(object):

    def __init__(self, owner, type_manager, connections, type):
        assert isinstance(connections, dict)
        self._owner = owner
        self._type_manager = type_manager
        self._connections = connections
        self._type = type

    def __len__(self):
        return len(self._connections[self._type.name])

    def __eq__(self, other):
        return self._connections[self._type.name] == other

    def __neq__(self, other):
        return self._connections[self._type.name] != other

    def __getattr__(self, name):
        if '_type_manager' not in self.__dict__:
            return

        type = self._type_manager.get_type(name)

        if type:
            nodes = list()

            for node in self._connections[self._type.name]:
                nodes.append(getattr(node, type))

            return AccumulatorFacade(self._type_manager, nodes)

    def __setattr__(self, name, value):
        if '_connections' in self.__dict__ and '_type' in self.__dict__ and \
                self._type.name in self._connections:
            for node in self._connections[self._type.name]:
                setattr(node, name, value)
        else:
            super(ConnectionsFacade, self).__setattr__(name, value)

    def __getitem__(self, index):
        return self._connections[self._type.name][index]

    def empty(self):
        for node in self._connections[self._type.name]:
            complement_connection = getattr(node, self._type.complement)
            complement_connection.remove(node)

        self._connections[self._type.name].empty()

    def append(self, *items):
        """

        >>> node1, node2 = Node(), Node()
        >>>
        >>> node1.children.append(node2)
        >>>
        >>> assert node2 in node1.children
        >>> assert node1 in node2.parents
        """
        self._connections[self._type.name].append(*items)

        for item in items:
            item._connections[self._type.complement].append(self._owner)

    def remove(self, *items):
        self._connections[self._type.name].remove(*items)

        for item in items:
            item._connections.remove[self._type.complement](self._owner)

    def find(self, **rules):
        self._connections[self._type.name].find(**rules)


class TypeManager(object):

    class Type(object):

        def __init__(self, name, complement):
            self.name = name
            self.complement = complement

    def __init__(self, types):
        self._types = dict()

        for name, complement in types.items():
            if name:
                self._types[name] = self.Type(name, complement)

            if complement:
                self._types[complement] = self.Type(complement, name)

    def get_type(self, name):
        if name in self._types:
            return self._types[name]

    @property
    def types(self):
        return self._types.keys()


# TODO: test _types via concrete nodes!
class Node(object):
    _types = {}

    def __init__(self):
        self._type_manager = TypeManager(self._types)

        self._connections = dict()
        for type in self._type_manager.types:
            self._connections[type] = Connections()

    def __getattr__(self, name):
        type = self._type_manager.get_type(name)

        if type:
            return ConnectionsFacade(self, self._type_manager,
                self._connections, type)

        return super(Node, self).__getattr__(name)

    def __setattr__(self, name, value):
        """ Assignment of children/parents resets previous content and creates
        needed links to nodes. Otherwise setting attributes works as expected.

        Simple assignment

        >>> node1, node2 = Node(), Node()
        >>> node1.children = node2
        >>>
        >>> assert node1.children[0] == node2

        Tuple assignment

        >>> node1, node2, node3 = Node(), Node(), Node()
        >>> node1.children = (node2, node3)
        >>>
        >>> assert node1.children[0] == node2
        >>> assert node1.children[1] == node3

        Assign value to an attribute

        >>> node = Node()
        >>>
        >>> node.value = 13
        >>> assert node.value == 13
        """

        def connection_template():
            if hasattr(self, name):
                connection = getattr(self, name)

                if connection:
                    connection._set_content(value)
            else:
                super(Node, self).__setattr__(name, value)

        if name in self._types.keys():
            connection_template()
        else:
            super(Node, self).__setattr__(name, value)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
