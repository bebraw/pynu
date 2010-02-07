Graph API
=========

BidiGraphNode
-------------

Bidirectional (if a link is created, it's considered two way always).

Note that in this case link access happens via 'connections'!

.. graphviz::

   graph bidigraphnode {
      "node1" -- "node2a";
      "node1" -- "node2b";
      "node2a" -- "node3a";
      "node2a" -- "node3b";
   }

DiGraphNode
-----------

Directional (ie. node1.parents = node2 does not mean that node1 is a child of
node2)

.. graphviz::

    digraph digraphnode {
        "bar" -> "baz";
    }

