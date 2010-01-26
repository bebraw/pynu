Overview of Pynu (Python Node Utilities)
========================================

The library offers two helper classes, GraphNode and TreeNode. TreeNode can be
considered to be a special case of a GraphNode. A TreeNode may have only one
parent at a time. In addition it provides functionality to find the root of the
tree (find_root) and to walk through each node of the tree based on the node
used as a pivot.

Node
----

Both GraphNode and TreeNode have been derived from Node that provides following
functionality:

.. automethod:: pynu.node.Node.__setattr__

.. automethod:: pynu.node.NodeContainer.empty

.. automethod:: pynu.node.NodeContainer.append

.. automethod:: pynu.node.NodeContainer.remove

.. automethod:: pynu.node.NodeContainer.find

GraphNode
---------

Currently GraphNode does not provide any extra functionality.

TreeNode
--------

TreeNode provides following utility methods:

.. autoclass:: pynu.TreeNode
    :members:
    :inherited-members:
