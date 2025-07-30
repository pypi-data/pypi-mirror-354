from scipy.spatial.distance import squareform
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
import random

def alter_distances(distances, max_amount=0):
    if max_amount == 0:
        max_amount = np.std(distances) / 50
    changer = lambda t: t + random.uniform(0, max_amount)
    return np.array([changer(d) for d in distances])

def calculate_mst(distances):
    X = csr_matrix(squareform(distances))
    mst = minimum_spanning_tree(X)
    return np.nonzero(mst)

def add_mst_to_links(links, mst):
    for i in range(0,len(mst[0])):
        # links.append('{"source":' + str(mst[0][i]) + ', "target":' + str(mst[1][i]) + '}')
        links.append([mst[0][i], mst[1][i]])
    return links

def multi_mst(distances, nr_msts=10):
    """
    Generate multiple minimum spanning trees from the given distances.
    """
    links = []
    for _ in range(nr_msts):
        altered_distances = alter_distances(distances)
        mst = calculate_mst(altered_distances)
        add_mst_to_links(links, mst)
    return links