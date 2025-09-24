# Basic LangGraph Code

class Node:
    def __init__(self, value):
        self.value = value
        self.edges = []

    def add_edge(self, node):
        self.edges.append(node)

    def __repr__(self):
        return f"Node({self.value})"

class LangGraph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, value):
        if value not in self.nodes:
            self.nodes[value] = Node(value)

    def add_edge(self, from_value, to_value):
        if from_value in self.nodes and to_value in self.nodes:
            self.nodes[from_value].add_edge(self.nodes[to_value])

    def display(self):
        for node in self.nodes.values():
            edges = [edge.value for edge in node.edges]
            print(f"{node.value} -> {edges}")

# Example usage
if __name__ == "__main__":
    graph = LangGraph()
    graph.add_node("Python")
    graph.add_node("Java")
    graph.add_node("C++")
    graph.add_edge("Python", "Java")
    graph.add_edge("Python", "C++")
    graph.display()
