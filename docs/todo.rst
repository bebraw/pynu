TODO
====

* Replace find with jQueryish syntax. (Add this for chaining too.)
* Make it possible to set attributes of connections (chaining too).
* Figure out nice syntax for setting edge attributes (ie. weights etc.).
  node1.connections.append(node2, label='foo', weight=1.5) ? How to access?
  node1.connections[node2].label? node2 = node1.connections[0]; node2.value = 5
* Implement shortest path algo (Dijkstra) (shortest_path(node1, node2)) ? ->
  this needs edge weights! -> add additional structure that allows to set them?
  it would be possible to expect that each edge has weight of 1 by default
* Get rid of the doctest __main__ blocks (implement proper test runner!)
