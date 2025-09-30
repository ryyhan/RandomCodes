# Orchestrator Agent with Sub-Agents: RAG, SQL, and MCP

class Node:
    def __init__(self, name):
        self.name = name
        self.behaviors = []

    def add_behavior(self, behavior):
        self.behaviors.append(behavior)

    def act(self, *args, **kwargs):
        for behavior in self.behaviors:
            behavior(self, *args, **kwargs)

    def __repr__(self):
        return f"Node({self.name})"

class LangGraph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)

    def connect(self, from_name, to_name):
        if from_name in self.nodes and to_name in self.nodes:
            # Orchestrator can trigger sub-agents
            self.nodes[from_name].add_behavior(lambda node, target=self.nodes[to_name]: target.act())

    def trigger(self, node_name, *args, **kwargs):
        if node_name in self.nodes:
            self.nodes[node_name].act(*args, **kwargs)

# Example: Orchestrator Agent with Sub-Agents
if __name__ == "__main__":
    graph = LangGraph()

    # Adding agents
    graph.add_node("Orchestrator")
    graph.add_node("RAG Agent")
    graph.add_node("SQL Agent")
    graph.add_node("MCP Agent")

    # Connecting orchestrator to sub-agents
    graph.connect("Orchestrator", "RAG Agent")
    graph.connect("Orchestrator", "SQL Agent")
    graph.connect("Orchestrator", "MCP Agent")

    # Defining behaviors for sub-agents
    def rag_behavior(node):
        print(f"{node.name} is retrieving relevant documents.")

    def sql_behavior(node):
        print(f"{node.name} is querying the database.")

    def mcp_behavior(node):
        print(f"{node.name} is interacting with the MCP server.")

    # Assigning behaviors to sub-agents
    graph.nodes["RAG Agent"].add_behavior(rag_behavior)
    graph.nodes["SQL Agent"].add_behavior(sql_behavior)
    graph.nodes["MCP Agent"].add_behavior(mcp_behavior)

    # Triggering orchestrator
    print("Orchestrator triggering sub-agents:")
    graph.trigger("Orchestrator")
