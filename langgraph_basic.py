# Orchestrator Agent with Dynamic Sub-Agent Selection

class Node:
    def __init__(self, name):
        self.name = name
        self.behaviors = {}

    def add_behavior(self, query_type, behavior):
        self.behaviors[query_type] = behavior

    def act(self, query_type, *args, **kwargs):
        if query_type in self.behaviors:
            self.behaviors[query_type](self, *args, **kwargs)
        else:
            print(f"{self.name} has no behavior for query type: {query_type}")

    def __repr__(self):
        return f"Node({self.name})"

class LangGraph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)

    def trigger(self, node_name, query_type, *args, **kwargs):
        if node_name in self.nodes:
            self.nodes[node_name].act(query_type, *args, **kwargs)

# Example: Orchestrator Agent with Dynamic Sub-Agent Selection
if __name__ == "__main__":
    graph = LangGraph()

    # Adding agents
    graph.add_node("Orchestrator")
    graph.add_node("RAG Agent")
    graph.add_node("SQL Agent")
    graph.add_node("MCP Agent")

    # Defining behaviors for sub-agents
    def rag_behavior(node):
        print(f"{node.name} is retrieving relevant documents.")

    def sql_behavior(node):
        print(f"{node.name} is querying the database.")

    def mcp_behavior(node):
        print(f"{node.name} is interacting with the MCP server.")

    # Assigning behaviors to sub-agents based on query type
    graph.nodes["RAG Agent"].add_behavior("retrieve", rag_behavior)
    graph.nodes["SQL Agent"].add_behavior("query", sql_behavior)
    graph.nodes["MCP Agent"].add_behavior("interact", mcp_behavior)

    # Orchestrator dynamically selects sub-agent based on query type
    def orchestrator_behavior(node, query_type):
        print(f"{node.name} received query type: {query_type}")
        if query_type == "retrieve":
            graph.trigger("RAG Agent", query_type)
        elif query_type == "query":
            graph.trigger("SQL Agent", query_type)
        elif query_type == "interact":
            graph.trigger("MCP Agent", query_type)
        else:
            print(f"{node.name} cannot handle query type: {query_type}")

    graph.nodes["Orchestrator"].add_behavior("dynamic", orchestrator_behavior)

    # Example queries
    print("Dynamic Orchestrator Example:")
    graph.trigger("Orchestrator", "dynamic", "retrieve")
    graph.trigger("Orchestrator", "dynamic", "query")
    graph.trigger("Orchestrator", "dynamic", "interact")
    graph.trigger("Orchestrator", "dynamic", "unknown")
