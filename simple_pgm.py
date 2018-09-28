import numpy

# inverts dictionary of edges
def invert(d):
    try:
        inv_d = {}
        for vertex, edge_list in d:
            for neighbour in edge_list:
                if not neighbour in inv_d:
                    inv_d[neighbour] = []

                inv_d[neighbour].append(vertex)

    except TypeError:
        raise


class bayesian_network:

    def __init__(self, vertices, ancestor_dict, distribution_dict):
        self.vertices = []
        for vertex in vertices:
            self.vertices.append(bayesian_node(self, vertex, ancestor_dict[vertex], distribution_dict[vertex]))

        self.edges = invert(ancestor_dict)

class bayesian_node:

    def __init__(self, population, name, ancestors, distribution):
        self.population = population
        self.name = name
        self.ancestors = ancestors
        self.distribution = distribution