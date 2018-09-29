import numpy as np
import itertools


# create uniform random distribution
def create_rand_distribution(shape):
    return np.random.rand(*shape)


# inverts dictionary of edges
def invert(edge_dict):
    try:
        inverted_dict = {}
        for vertex in edge_dict:
            edge_list = edge_dict[vertex]
            for neighbour in edge_list:
                if neighbour not in inverted_dict:
                    inverted_dict[neighbour] = []
                inverted_dict[neighbour].append(vertex)
    except TypeError:
        raise


class BayesianNetwork:
    def __init__(self, vertices, ancestors_dict, eventlist_dict):
        self.vertices = {}

        # create vertices and set individual events
        for vertex in vertices:
            self.vertices[vertex] = BayesianNode(self, vertex)
            self.vertices[vertex].set_events(eventlist_dict[vertex])

        # set ancestors
        for vertex in vertices:
            self.vertices[vertex].set_ancestors(ancestors_dict[vertex])

        # invert ancestors_dict to get the edges
        self.edges = invert(ancestors_dict)

    # assign distributions for each vertex
    def set_distributions(self, distribution_dict):
        for vertex in self.vertices:
            vertex.set_distribution(distribution_dict[vertex])

    # return the probability of an event
    def probability(self, event_dict):
        assert len(event_dict) == len(self.vertices)

        currprob = 1
        for vertex, event in event_dict:
            currprob *= self.vertices[vertex].probability(event_dict)


class BayesianNode:
    def __init__(self, population, name):
        self.population = population
        self.name = name
        self.events = []
        self.ancestors = []
        self.ancestors_events = []
        self.events_map = {}
        self.ancestors_events_map = {}

    # get number of events
    def num_events(self):
        return len(self.events)

    # get number of ancestors
    def num_ancestors(self):
        return len(self.ancestors)

    # get shape of own distribution
    def distribution_shape(self):
        return (len(self.events_map), len(self.ancestors_events_map))

    # feed in events
    def set_events(self, events):
        self.events = sorted(events)
        self.events_map = {event: index for index, event in enumerate(self.events)}

    # assign ancestors
    def set_ancestors(self, ancestors):
        self.ancestors = sorted(ancestors)
        self.ancestors_events = list(itertools.product(*[self.population.vertices[ancestor].events for ancestor in self.ancestors]))
        self.ancestors_events_map = {event_tuple: index for index, event_tuple in enumerate(self.ancestors_events)}

    # feed in distribution
    def set_distribution(self, distribution):
        self.distribution = distribution

    # find probability according to our distribution
    def probability(self, event_dict):
        ancestor_events = tuple(event_dict[ancestor] for ancestor in self.ancestors)
        event = event_dict[self.name]

        return self.distribution[self.event_map[event]][self.ancestor_events_map[ancestor_events]]


if __name__ == '__main__':
    num_vertices = 10
    assert num_vertices > 0

    # vertices 1 to n
    vertex_indices = list(range(1, num_vertices + 1))

    # create dict of events - same here for every vertex for simplicity
    eventlist_dict = {vertex_index: ['A', 'B', 'C'] for vertex_index in vertex_indices}

    # create random list of ancestors for each vertex
    ancestors_dict = {}
    for vertex in range(1, num_vertices + 1):
        rand_size = np.random.randint(0, num_vertices)
        ancestor_list = []

        for _ in range(rand_size):
            rand_entry = np.random.randint(1, num_vertices + 1)
            while rand_entry == vertex or rand_entry in ancestor_list:
                rand_entry = np.random.randint(1, num_vertices + 1)
            ancestor_list.append(rand_entry)

        ancestors_dict[vertex] = ancestor_list

    # create Bayesian Network! :)
    G = BayesianNetwork(vertex_indices, ancestors_dict, eventlist_dict)

    # set distributions
    for vertex_index in G.vertices:
        vertex = G.vertices[vertex_index]
        vertex.set_distribution(create_rand_distribution(vertex.distribution_shape()))
