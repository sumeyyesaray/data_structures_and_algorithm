import matplotlib.pyplot as plt  # Used for visualizing graphs
import networkx as nx  # Used for visualizing graphs


class Vertex:
    def __init__(self, key):
        self.key = key
        self.neighbors = {}

    def get_neighbor(self, other):
        return self.neighbors.get(other, None)

    def set_neighbor(self, other, weight=0):
        self.neighbors[other] = weight

    def __repr__(self):
        return f"Vertex({self.key})"

    def __str__(self):
        return (
                str(self.key)
                + " connected to: "
                + str([x.key for x in self.neighbors])
        )

    def get_neighbors(self):
        return self.neighbors.keys()

    def get_key(self):
        return self.key


class Graph:
    def __init__(self):
        self.vertices = {}

    def set_vertex(self, key):
        self.vertices[key] = Vertex(key)

    def get_vertex(self, key):
        return self.vertices.get(key, None)

    def __contains__(self, key):
        return key in self.vertices

    def add_edge(self, from_vert, to_vert, weight=0):
        if from_vert not in self.vertices:
            self.set_vertex(from_vert)
        if to_vert not in self.vertices:
            self.set_vertex(to_vert)
        self.vertices[from_vert].set_neighbor(self.vertices[to_vert], weight)

    def get_vertices(self):
        return self.vertices.keys()

    def __iter__(self):
        return iter(self.vertices.values())


def bfs(graph, start_key):
    if start_key not in graph.vertices:
        print("Start vertex not in graph!")
        return

    visited = set()
    queue = [start_key]  # Using a list as a queue
    visited.add(start_key)

    while queue:
        current_key = queue.pop(0)  # Dequeue the first element (FIFO)
        print(current_key, end=" ")  # Process the vertex

        current_vertex = graph.get_vertex(current_key)
        for neighbor in current_vertex.get_neighbors():
            neighbor_key = neighbor.get_key()
            if neighbor_key not in visited:
                visited.add(neighbor_key)
                queue.append(neighbor_key)  # Enqueue the neighbor


def dfs_recursive(graph, start_key, visited=None):
    if visited is None:
        visited = set()

    if start_key not in graph.vertices:
        print("Start vertex not in graph!")
        return

    visited.add(start_key)
    print(start_key, end=" ")  # Process the vertex

    current_vertex = graph.get_vertex(start_key)
    for neighbor in current_vertex.get_neighbors():
        neighbor_key = neighbor.get_key()
        if neighbor_key not in visited:
            dfs_recursive(graph, neighbor_key, visited)


def dfs_iterative(graph, start_key):
    if start_key not in graph.vertices:
        print("Start vertex not in graph!")
        return

    visited = set()
    stack = [start_key]  # Using a list as a stack

    while stack:
        current_key = stack.pop()  # Pop the last element (LIFO)
        if current_key not in visited:
            visited.add(current_key)
            print(current_key, end=" ")  # Process the vertex

            current_vertex = graph.get_vertex(current_key)
            for neighbor in current_vertex.get_neighbors():
                neighbor_key = neighbor.get_key()
                if neighbor_key not in visited:
                    stack.append(neighbor_key)  # Push the neighbor onto the stack


def bfs_spanning_tree(graph, start_key):
    """
    Generate the BFS spanning tree as a list of edges.
    """
    if start_key not in graph.vertices:
        print("Start vertex not in graph!")
        return []

    visited = set()
    queue = [start_key]
    visited.add(start_key)
    spanning_tree = []

    while queue:
        current_key = queue.pop(0)
        current_vertex = graph.get_vertex(current_key)

        for neighbor in current_vertex.get_neighbors():
            neighbor_key = neighbor.get_key()
            if neighbor_key not in visited:
                visited.add(neighbor_key)
                queue.append(neighbor_key)
                spanning_tree.append((current_key, neighbor_key))

    return spanning_tree


def dfs_spanning_tree(graph, start_key):
    """
    Generate the DFS spanning tree as a list of edges.
    """

    def dfs_helper(vertex_key, visited, spanning_tree):
        visited.add(vertex_key)
        current_vertex = graph.get_vertex(vertex_key)

        for neighbor in current_vertex.get_neighbors():
            neighbor_key = neighbor.get_key()
            if neighbor_key not in visited:
                spanning_tree.append((vertex_key, neighbor_key))
                dfs_helper(neighbor_key, visited, spanning_tree)

    if start_key not in graph.vertices:
        print("Start vertex not in graph!")
        return []

    visited = set()
    spanning_tree = []
    dfs_helper(start_key, visited, spanning_tree)
    return spanning_tree


def visualize_graph_and_trees(graph, bfs_tree, dfs_tree):
    """
    Plot the original graph, BFS tree, and DFS tree side by side.

    Parameters:
    - graph: The original graph (Graph class).
    - bfs_tree: List of edges representing the BFS tree.
    - dfs_tree: List of edges representing the DFS tree.
    """
    # Create NetworkX representations for graph, BFS tree, and DFS tree
    original_graph = nx.DiGraph()  # Use nx.Graph() for undirected graphs
    bfs_graph = nx.DiGraph()
    dfs_graph = nx.DiGraph()

    # Add edges for the original graph
    for vertex in graph:
        for neighbor in vertex.get_neighbors():
            weight = vertex.get_neighbor(neighbor)
            original_graph.add_edge(vertex.get_key(), neighbor.get_key(), weight=weight)

    # Add edges for BFS and DFS trees
    bfs_graph.add_edges_from(bfs_tree)
    dfs_graph.add_edges_from(dfs_tree)

    # Plot layout
    pos = nx.spring_layout(original_graph)  # Use the same layout for all graphs

    # Create subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Graph and Search Trees", fontsize=16)

    # Plot Original Graph
    nx.draw(
        original_graph,
        pos,
        ax=axes[0],
        with_labels=True,
        node_size=2000,
        node_color='lightblue',
        font_size=12,
        font_weight='bold',
    )
    axes[0].set_title("Original Graph")

    # Plot BFS Tree
    nx.draw(
        bfs_graph,
        pos,
        ax=axes[1],
        with_labels=True,
        node_size=2000,
        node_color='lightgreen',
        font_size=12,
        font_weight='bold',
    )
    axes[1].set_title("BFS Tree (Reflects the level-order traversal of nodes)")

    # Plot DFS Tree
    nx.draw(
        dfs_graph,
        pos,
        ax=axes[2],
        with_labels=True,
        node_size=2000,
        node_color='lightcoral',
        font_size=12,
        font_weight='bold',
    )
    axes[2].set_title("DFS Tree (Shows the depth-first exploration path)")

    # Show the plots
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout for the title
    plt.show()


def main():
    # Create a graph and add vertices and edges
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('C', 'F')
    g.add_edge('E', 'F')
    g.add_edge('F', 'G')
    g.add_edge('D', 'G')
    g.add_edge('G', 'A')
    g.add_edge('C', 'E')
    g.add_edge('E', 'B')

    # BFS Traversal
    print("BFS Traversal:")
    bfs(g, 'A')

    print("\n\nDFS Traversal (Recursive):")
    dfs_recursive(g, 'A')

    print("\n\nDFS Traversal (Iterative):")
    dfs_iterative(g, 'A')

    # Generate BFS and DFS spanning trees
    bfs_tree = bfs_spanning_tree(g, 'A')
    dfs_tree = dfs_spanning_tree(g, 'A')

    # Visualize the original graph and both trees
    visualize_graph_and_trees(g, bfs_tree, dfs_tree)


if __name__ == '__main__':
    main()
