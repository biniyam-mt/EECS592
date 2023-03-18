#!/usr/bin/env python3

# EECS 592 Homework 3

from pprint import pprint
import json
import random


class TupleError(Exception):
    """Raise when tuple is not present in conditional probability dictionary.
    This is here mainly for students to catch their own errors.
    """

    def __init__(self, name):
        super().__init__(
            "Error: Tuple not present in conditional probability dictionary of Node "
            + name
        )


class Node:
    """A node in the bayesian network.
    Please read all comments in this class.
    """

    nodes = {}  # Static object: use this to access any existing node

    # REMEMBER TO RESET THIS if you would like to use a different JSON file
    def __init__(self, name):
        self.name = name  # string
        self.parents = []  # list of parent names
        self.children = []  # list of children names
        self.condProbs = {}  # (boolean tuple in parent names order) --> float
        self.prob = -1  # If no parent, use this
        Node.nodes[name] = self

    def sample(self, tup):
        """Sample based on boolean tuple passed in.
        Return bool of conditional event

        Arguments:
        tup -- boolean tuple, in order of self.parents
        """
        true_prob = self.prob
        # Usually not the root node in bayesian network
        if self.condProbs:
            if tup not in self.condProbs:
                raise TupleError(self.name)
            true_prob = self.condProbs[tup]
        return True if random.random() < true_prob else False


def topological():
    """Return list of Node names in topological order.
    The code here performs a topological sort on the nodes.
    """
    visited = set()
    top_sorted = []

    # Helper function to DFS over all children
    def visit(node_name):
        visited.add(node_name)
        for child_name in Node.nodes[node_name].children:
            if child_name not in visited:
                visit(child_name)
        # At this point, we have visited all children
        top_sorted.append(node_name)

    for node_name in Node.nodes:
        if node_name not in visited:
            visit(node_name)
    return top_sorted[::-1]


def rejection_sampling(query, evidence, totalSamples=10000):
    """Return estimated normalized prob distr of query.

    Arguments:
    query        -- node name (string)
    evidence     -- dictionary of node names (strings) --> boolean
    totalSamples -- total number of samples to generate (integer)
    """

    """YOUR CODE HERE."""


def likelihood_weighting(query, evidence, totalSamples=10000):
    """Return estimated normalized prob distr of query.

    Arguments:
    query    -- node name (string)
    evidence -- dictionary of node names (strings) --> boolean
    """
    """YOUR CODE HERE."""


def parse_file(filename):
    """Parse JSON file of bayesian network.

    JSON key-value pairs:
    "Name"         -- Name of the node.
    "Parents"      -- List of names of parent nodes.
                      Conditionals are given in order of this list.
    "Children"     -- List of names of child nodes.
    "Conditionals" -- Single float OR List of conditional probabilities.
                      **float for a root node, list of floats for a non-root node**
                      Indices are integer representation of bits (i.e. 0=FF, 1=FT, 2=TF, 3=TT).
                      Ordering of parents align with the bits here
                          i.e. parents = ['Sprinkler', 'Rain']
                               FT refers to Sprinkler=False, Rain=True
    """
    with open(filename, "r") as f:
        data = json.load(f)
        for node_data in data:
            node = Node(node_data["Name"])
            node.parents = node_data["Parents"]
            node.children = node_data["Children"]

            # A root node in bayesian network
            if type(node_data["Conditionals"]) is not list:
                node.prob = node_data["Conditionals"]

            # A non-root node in bayesian network
            else:
                # Parse bit representation of each index in the list
                for bits, prob in enumerate(node_data["Conditionals"]):
                    tup = []
                    for event in reversed(node.parents):
                        tup.append(bool(bits & 1))
                        bits = bits >> 1
                    node.condProbs[tuple(reversed(tup))] = prob


def main():
    random.seed()  # Unseeded

    # Weather BN
    parse_file("weather.json")

    # rejection_sampling('Rain', {'Sprinkler':True})
    # likelihood_weighting('Rain', {'Sprinkler':True})

    # Reset static member
    Node.nodes = {}

    # Alarm BN
    parse_file("alarm.json")


if __name__ == "__main__":
    main()
