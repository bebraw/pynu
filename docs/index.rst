===========================
Pynu - Node Utility Library
===========================

:Author: `Juho Vepsäläinen <http://nixtu.blogspot.com>`_
:Version: Pynu |version|
:Date: |today|
:Homepage: `Pynu Homepage`_
:License: `GPLv3 License`_
:Contact: bebraw@gmail.com

.. _Pynu Homepage: http://github.com/bebraw/pynu
.. _GPLv3 License: http://www.gnu.org/licenses/gpl-3.0.html


.. module:: mock
   :synopsis: Mock object and testing library.

The library offers two helper classes, DirectedGraphNode and TreeNode. TreeNode
can be considered to be a special case of a DirectedGraphNode. A TreeNode may
have only one parent at a time. In addition it provides functionality to find
the root of the tree (find_root) and to walk through each node of the tree
based on the node used as a pivot.

API Documentation
-----------------

.. toctree::
    :maxdepth: 2

    graph_api
    tree_api

User Documentation
------------------

.. toctree::
    :maxdepth: 2

    changelog

Developer Documentation
-----------------------

.. toctree::
    :maxdepth: 2

    todo
    dev_guide


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
