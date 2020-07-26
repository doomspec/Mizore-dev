class Node:
    def __init__(self, name):
        """
        Constructor for node
        Args:
            name: name of node
        """
        self.name = name
        self.weight_map = {}
        self.neighbors = set()

    def add_neighbor(self, node, weight):
        """
        Build Edge
        Args:
            node: neighbor node
            weight: weight between neighbor node and self
        Returns: None
        """
        name = node.name
        self.weight_map[name] = weight
        self.neighbors.add(node)

    def find_weight(self, node):
        """
        Find the weight of node
        Args:
            node: target node

        Returns: weight to the target node

        """
        name = node.name
        assert self.weight_map.__contains__(name)
        return self.weight_map[name]

    def has_neighbor(self, node):
        """

        Args:
            node: neighbor node

        Returns: whether has this neighbor

        """
        return self.neighbors.__contains__(node)
