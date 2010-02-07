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

Getting the first child:

    >>> node1.children[0]
    node2a

Getting the last child:

    >>> node1.children[-1]
    node2b

Getting the parent:

    >>> node3a.parent
    node2a

Note that the root node doesn't have a parent.

    >>> node1.parent
    None

Finding a child with specific property (works for parent too):

    >>> node3a.color = 'blue'
    >>> node1.children('color=blue')
    node3a

If multiple results are found, results are returned in finding order. Note that
it is possible to use a regex pattern in the search.

    >>> node2a.color = 'black'
    >>> node1.children('color=^bl')
    [node2a, node3a]

Manipulation
^^^^^^^^^^^^

Setting an attribute:

    >>> node2a.width = 200

Setting attribute to multiple nodes at once:
Note that the selector matches
any node that has a color attribute.

    >>> node1.children('color=.').height = 100
    >>> node2a.height
    100
    >>> node3a.height
    100

Adding nodes to structure:

    >>> node4a, node4b = TreeNode(), TreeNode()
    >>> node3a.children = node4a
    >>> node3a.append(node4b)

This works as well:

    >>> node3a.children = (node4a, node4b)

Removing nodes from structure.

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
