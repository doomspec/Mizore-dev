from Benchmark.node import Node
from Benchmark.edge import Edge


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.node_dict = {}
        self.node_edge_dict = {}

    def add_node(self, name):
        name = str(name)
        if self.node_dict.__contains__(name):
            return self.node_dict[name]
        node = Node(name)
        self.nodes.add(node)
        self.node_dict[name] = node
        return node

    def add_edge(self, from_node, to_node, weight):
        if isinstance(from_node, str) or isinstance(from_node, int):
            from_node = self.add_node(from_node)
        if isinstance(to_node, str) or isinstance(to_node, int):
            to_node = self.add_node(to_node)
        assert isinstance(from_node, Node)
        assert isinstance(to_node, Node)
        from_node_name = from_node.name
        to_node_name = to_node.name
        edge = Edge(from_node, to_node, weight)
        if not self.node_edge_dict.__contains__(from_node_name):
            self.node_edge_dict[from_node_name] = {}
        if not self.node_edge_dict[from_node_name].__contains__(to_node_name):
            self.node_edge_dict[from_node_name][to_node_name] = edge
            self.edges.add(edge)
        from_node.add_neighbor(to_node, weight)
        edge = self.node_edge_dict[from_node_name][to_node_name]
        edge.weight = weight
        return edge


def generate_graph_node_dict(graph):
    """Generates a dictionary containing key:value pairs in the form of
                    Graph node : integer index of the node

    Args:
        graph: Graph object

    Returns:
        A dictionary as described
    """
    nodes_int_map = []
    for node_index, node in enumerate(graph.nodes):
        nodes_int_map.append((node, node_index))
    nodes_dict = dict(nodes_int_map)
    return nodes_dict
