# -*- coding: utf-8 -*-
"""
Facade classes.
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
        connection_type = self._type_manager.get_type(name)

        if connection_type:
            nodes = list()

            for node in self._nodes:
                nodes.append(getattr(node, connection_type))

            return AccumulatorFacade(self._type_manager, nodes,
                connection_type)

    def __setattr__(self, name, value):
        if '_nodes' in self.__dict__:
            for node in self._nodes:
                setattr(node, name, value)
        else:
            super(AccumulatorFacade, self).__setattr__(name, value)

# TODO: test and fix simple assigment (ie. node1.children = node2)
# handle accum set (ie. node.parents.parents.color = 'blue' should set color of
# all belonging to that selection)
# handle node.parents.parents.find(color='blue')
class ConnectionsFacade(object):

    def __init__(self, owner, type_manager, connections, connection_type):
        assert isinstance(connections, dict)
        self._owner = owner
        self._type_manager = type_manager
        self._connections = connections
        self._connection_type = connection_type

    def __len__(self):
        return len(self._connections[self._connection_type.name])

    def __eq__(self, other):
        return self._connections[self._connection_type.name] == other

    def __neq__(self, other):
        return self._connections[self._connection_type.name] != other

    def __getattr__(self, name):
        if '_type_manager' not in self.__dict__:
            return

        connection_type = self._type_manager.get_type(name)

        if connection_type:
            nodes = list()

            for node in self._connections[self._connection_type.name]:
                nodes.append(getattr(node, connection_type))

            return AccumulatorFacade(self._type_manager, nodes)

    def __setattr__(self, name, value):
        if '_connections' in self.__dict__ and \
                '_connection_type' in self.__dict__ and \
                self._connection_type.name in self._connections:
            for node in self._connections[self._connection_type.name]:
                setattr(node, name, value)
        else:
            super(ConnectionsFacade, self).__setattr__(name, value)

    def __getitem__(self, index):
        return self._connections[self._connection_type.name][index]

    def empty(self):
        for node in self._connections[self._connection_type.name]:
            complement_connection = getattr(node,
                self._connection_type.complement)
            complement_connection.remove(node)

        self._connections[self._connection_type.name].empty()

    def append(self, *items):
        """

        >>> node1, node2 = Node(), Node()
        >>>
        >>> node1.children.append(node2)
        >>>
        >>> assert node2 in node1.children
        >>> assert node1 in node2.parents
        """
        self._connections[self._connection_type.name].append(*items)

        for item in items:
            item._connections[self._connection_type.complement].append(
                self._owner)

    def remove(self, *items):
        self._connections[self._connection_type.name].remove(*items)

        for item in items:
            item._connections.remove[self._connection_type.complement](
                self._owner)

    def find(self, **rules):
        return self._connections[self._connection_type.name].find(
            self._connection_type.name, **rules)

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()