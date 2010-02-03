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


class Connections(list):

    def __init__(self, owner=None, nodes=[]):
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
        >>> con1.append('foo')
        >>> con2.append('bar')
        >>>
        >>> assert con1 != con2
        """
        return not self == other

    def empty(self):
        """Empties content.

        >>> con1, con2 = Connections(), Connections()
        >>>
        >>> con1.append(con2)
        >>>
        >>> assert len(con1) == 1
        >>>
        >>> con1.empty()
        >>>
        >>> assert len(con1) == 0
        """
        for node in self:
            self.remove(node)

    def append(self, *items):
        """Appends given items connections.

        Regular case

        >>> con1, con2 = Connections(), Connections()
        >>>
        >>> con1.append(con2)
        >>>
        >>> assert con1[0] == con2

        Append multiple times (retains only one reference to target!)

        >>> con1, con2 = Connections(), Connections()
        >>> con1.append(con2)
        >>> con1.append(con2)
        >>>
        >>> assert con1[0] == con2
        >>> assert len(con1) == 1

        Append multiple at once

        >>> con1, con2, con3 = Connections(), Connections(), Connections()
        >>>
        >>> con1.append(con2, con3)
        >>>
        >>> assert len(con1) == 2
        >>> assert con2 in con1
        >>> assert con3 in con1
        """
        for item in items:
            for node in self:
                if item is node:
                    return

            super(Connections, self).append(item)

    def remove(self, *items):
        """Removes given items from connections.

        Regular case

        >>> con1, con2 = Connections(), Connections()
        >>>
        >>> con1.append(con2)
        >>> con1.remove(con2)
        >>>
        >>> assert len(con1) == 0

        Remove multiple times

        >>> con1, con2 = Connections(), Connections()
        >>>
        >>> con1.append(con2)
        >>> con1.remove(con2)
        >>> con1.remove(con2)
        >>> con1.remove(con2)
        >>>
        >>> assert len(con1) == 0

        Remove multiple at once

        >>> con1, con2, con3 = Connections(), Connections(), Connections()
        >>>
        >>> con1.append(con2, con3)
        >>>
        >>> assert len(con1) == 2
        >>>
        >>> con1.remove(con2, con3)
        >>>
        >>> assert len(con1) == 0
        """
        for item in items:
            if item in self:
                super(Connections, self).remove(item)


class Finder(object):

    def find(self, connection_type, **rules):
        """Finds and returns content matching to given rules.
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
