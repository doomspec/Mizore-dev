class City:
    def __init__(self, name):
        """
        Constructor for city
        Args:
            name: name of city
        """
        self.name = name
        self.distance_map = {}
        self.neighbors = set()

    def add_neighbor(self, city, distant):
        """
        Build Edge
        Args:
            city: neighbor city
            distant: distance between neighbor city and self
        Returns: None
        """
        name = city.name
        self.distance_map[name] = distant
        self.neighbors.add(city)

    def find_distance(self, city):
        """
        Find the distance of city
        Args:
            city: target city

        Returns: distance to the target city

        """
        name = city.name
        assert self.distance_map.__contains__(name)
        return self.distance_map[name]

    def has_neighbor(self,city):
        """

        Args:
            city: neighbor city

        Returns: whether has this neighbor

        """
        return self.neighbors.__contains__(city)