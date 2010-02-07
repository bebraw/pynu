TreeNode
========

.. testsetup:: *

    from pynu import TreeNode

    node1, node2a, node2b = TreeNode(), TreeNode(), TreeNode()
    node3a, node3b = TreeNode(), TreeNode()

    node1.children = (node2a, node2b)
    node2a.children = (node3a, node3b)

Graph
^^^^^

.. graphviz::

   graph tree {
      "node1" -- "node2a";
      "node1" -- "node2b";
      "node2a" -- "node3a";
      "node2a" -- "node3b"
   }

Setting Up the Graph
^^^^^^^^^^^^^^^^^^^^

.. doctest::

    >>> from pynu import TreeNode

    >>> node1, node2a, node2b = TreeNode(), TreeNode(), TreeNode()
    >>> node3a, node3b = TreeNode(), TreeNode()

    >>> node1.children = (node2a, node2b)
    >>> node2a.children = (node3a, node3b)

Traversal
^^^^^^^^^

Getting the first child
""""""""""""""""""""""""

    >>> node1.children[0]
    node2a

Getting the last child
""""""""""""""""""""""

    >>> node1.children[-1]
    node2b

This works for the parent attribute too.

    >>> node3a.parent
    node2a

Note that the root node doesn't have a parent.

    >>> node1.parent
    None

Getting an entire level of children
"""""""""""""""""""""""""""""""""""

    >>> node1.children.children
    [node3a, node3b]

If node2b would have had children as well, they have shown up in the result
too.

Finding a child with specific property
""""""""""""""""""""""""""""""""""""""

    >>> node2a.color = 'blue'
    >>> node1.children('color=blue')
    node2a

Note that this works for parent too.

    >>> node3a.parent('color=blue')
    node2a

If multiple results are found, results are returned in finding order. Note that
it is possible to use a regex pattern in the search.

    >>> node3a.color = 'black'
    >>> node1.children('color=^bl')
    [node2a, node3a]

If no result is found, None is returned:

    >>> node1.children('color=red')
    None

Manipulation
^^^^^^^^^^^^

Setting an attribute
""""""""""""""""""""

    >>> node2a.width = 200

Setting an attribute to multiple nodes
""""""""""""""""""""""""""""""""""""""

Note that the selector matches any node that has a color attribute.

    >>> node1.children('color=.').height = 100
    >>> node2a.height
    100
    >>> node3a.height
    100

Setting an attribute to a whole level
"""""""""""""""""""""""""""""""""""""

    >>> node1.children.children.width = 150
    >>> node3a.width
    150
    >>> node3b.width
    150

Note that it's possible to alter an existing value as well.

    >>> node1.children.children.width -= 100
    >>> node3a.width
    50
    >>> node3b.width
    50

Adding nodes to the structure
"""""""""""""""""""""""""""""

    >>> node4a, node4b = TreeNode(), TreeNode()
    >>> node3a.children = node4a
    >>> node3a.children.append(node4b)

This works as well

    >>> node3a.children = (node4a, node4b)

Note that appending to parent should not work. In this case only assignment
should be used.

    >>> try:
    ...     node3a.parent.append(node3b)
    ... except AttributeError:
    ...     pass
    ... else:
    ...     assert False


Removing nodes from structure
"""""""""""""""""""""""""""""

    >>> assert len(node3a.children) == 2
    >>> node3a.children.remove(node4b)
    >>> assert len(node3a.children) == 1

FIXME: check that GC works ok with removed branches (make sure that ref count
goes to zero after remove).

Additional Methods
^^^^^^^^^^^^^^^^^^

.. autoclass:: pynu.TreeNode
    :members:
    :inherited-members:
