# Import deque from the collections module for efficient queue operations (FIFO)
from collections import deque

# Import NetworkX library for graph creation and manipulation
import networkx as nx

# Import Matplotlib for graph visualization
import matplotlib.pyplot as plt


# Define a class called BFSPlanner that will perform Breadth-First Search planning
class BFSPlanner:

    # Constructor method that initializes the planner with a graph
    def __init__(self, graph):
        self.graph = graph  # Store the graph structure (dictionary of nodes and neighbors)

    # Function to generate a plan (shortest path) from start node to goal node
    def plan(self, start, goal):

        """Finds the shortest plan from start to goal using BFS."""

        # Create a queue and initialize it with the starting path
        # deque is used because it allows fast popping from the left
        queue = deque([[start]])

        # Create a set to keep track of visited nodes to avoid revisiting
        visited = set()

        # Continue searching while the queue still has paths to explore
        while queue:

            # Remove the first path from the queue (FIFO behavior)
            path = queue.popleft()

            # Get the last node (current state) in the path
            state = path[-1]

            # If the current node is the goal, return the path as the solution
            if state == goal:
                return path

            # If the node has not yet been visited
            if state not in visited:

                # Mark the node as visited
                visited.add(state)

                # Look at all neighbors connected to the current node
                for neighbor in self.graph.get(state, []):

                    # Create a copy of the current path
                    new_path = list(path)

                    # Add the neighbor node to the new path
                    new_path.append(neighbor)

                    # Add the new path to the queue for future exploration
                    queue.append(new_path)

        # If no path to the goal is found, return None
        return None

    # Function to visualize the graph and highlight the discovered path
    def visualize_plan(self, path):

        """Draws the graph with the discovered path highlighted."""

        # Convert the dictionary graph into a NetworkX graph object
        G = nx.Graph(self.graph)

        # Generate positions for nodes using a spring layout algorithm
        # seed ensures the layout stays the same each time
        pos = nx.spring_layout(G, seed=42)

        # Set the figure size for better visualization
        plt.figure(figsize=(8, 6))

        # Draw the graph with labels and node styling
        nx.draw(
            G,                     # Graph object
            pos,                   # Node positions
            with_labels=True,     # Display node labels
            node_color="lightblue",  # Node color
            node_size=2200,       # Node size
            font_size=12          # Label font size
        )

        # If a valid path exists
        if path:

            # Convert the path nodes into edges (pairs of nodes)
            edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

            # Highlight the path edges in red
            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=edges,
                edge_color="red",
                width=3
            )

            # Add a title showing the optimal path found
            plt.title(f"Optimal Plan: {' → '.join(path)}", fontsize=13)

        # Display the graph visualization
        plt.savefig("output.png")


# Define a simple environment (graph world) as a dictionary
# Each location is connected to neighboring locations
world = {
    'Home': ['Bus Stop', 'Shop'],   # Home connects to Bus Stop and Shop
    'Bus Stop': ['Home', 'Office'], # Bus Stop connects to Home and Office
    'Shop': ['Home', 'Park'],       # Shop connects to Home and Park
    'Park': ['Shop', 'Office'],     # Park connects to Shop and Office
    'Office': ['Bus Stop', 'Park']  # Office connects to Bus Stop and Park
}

# Create an instance of the BFSPlanner with the world graph
planner = BFSPlanner(world)

# Generate a plan (shortest path) from Home to Office
path = planner.plan('Home', 'Office')

# Print the discovered path
print("Generated Plan:", path)

# Visualize the graph and highlight the BFS path
planner.visualize_plan(path)
