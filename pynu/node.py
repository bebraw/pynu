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


class Node(object):
    _types = {}

    def __init__(self):
        self._type_manager = TypeManager(self._types)

        self._connections = dict()
        for type in self._type_manager.types:
            self._connections[type] = Connections(owner=self)

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
