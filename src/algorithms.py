"""
This module provides algorithms that operate on objects of the `Graph` class
from the `graph` module. 

These are implemented as independent functions to keep the core data structure separate from algorithmic logic.

Implemented / planned algorithms include:
- Traversal
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)

- Pathfinding
  - Dijkstra's algorithm (shortest paths in weighted graphs)
  - Bellman-Ford algorithm (handles negative weights)
  - A* search (heuristic-guided shortest paths)

- Spanning Trees
  - Prim's algorithm
  - Kruskal's algorithm

- Connectivity
  - Connected components
  - Cycle detection
  - Graph is_connected check

Design notes:
- Algorithms ignore edge weights unless otherwise specified.
- All functions accept a `Graph` instance and relevant parameters
  (e.g., start node), and return results in Python-native structures
  such as lists, sets, or dictionaries.
"""
