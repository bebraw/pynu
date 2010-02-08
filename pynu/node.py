# -*- coding: utf-8 -*-
"""
Node classes.
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
from connection import Connections
from facade import ConnectionsFacade


class TypeManager(object):

    class Type(object):

        def __init__(self, name, complement, facades):
            self.name = name
            self.complement = complement

            if name in facades:
                self.facade = facades[name]
            else:
                self.facade = ConnectionsFacade

    def __init__(self, types, facades):
        self._types = dict()

        for name, complement in types.items():
            if name:
                self._types[name] = self.Type(name, complement, facades)

            if complement:
                self._types[complement] = self.Type(complement, name, facades)

    def get_facade(self, node, name):
        type = self.get_type(name)

        if type:
            return type.facade(node, self, node.connections, type)

    def get_type(self, name):
        if name in self._types:
            return self._types[name]

    @property
    def types(self):
        return self._types.keys()


class Node(object):
    _types = {}
    _facades = {}

    def __init__(self):
        self._type_manager = TypeManager(self._types, self._facades)

        self.connections = dict()
        for type in self._type_manager.types:
            self.connections[type] = Connections(owner=self)

    def __getattr__(self, name):
        return self._type_manager.get_facade(self, name)

    def __setattr__(self, name, value):
        """ Assignment of children/parents resets previous content and creates
        needed links to nodes. Otherwise setting attributes works as expected.

        Setup

        >>> Node._types = {'children': None}

        Simple assignment

        >>> node1, node2 = Node(), Node()
        >>>
        >>> assert isinstance(node1.children, ConnectionsFacade)
        >>> node1.children = node2
        >>> assert isinstance(node1.children, ConnectionsFacade)
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
        if name == '_type_manager':
            super(Node, self).__setattr__(name, value)
        elif name in self._type_manager.types:
            connection = getattr(self, name)
            connection._set_content(value)
        else:
            super(Node, self).__setattr__(name, value)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
