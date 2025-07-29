"""
synth-graph: Modern graph orchestration library for LLMs
"""

__version__ = "0.1.0"

# Placeholder for main API
class Graph:
    """Main graph interface."""
    
    def __init__(self):
        self.nodes = {}
        self.edges = []
        
    def add_node(self, name, node):
        """Add a node to the graph."""
        self.nodes[name] = node
        
    def add_edge(self, from_node, to_node):
        """Add an edge between nodes."""
        self.edges.append((from_node, to_node))
        
    def run(self, input_data):
        """Execute the graph."""
        raise NotImplementedError("Coming soon!")


class Node:
    """Graph node."""
    
    def __init__(self, fn):
        self.fn = fn


__all__ = ["Graph", "Node"]