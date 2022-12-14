import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import json


def generate_graph(node, vertices):
    """
    This function creates the connected peer to peer network of the bazaar randomly by taking number of nodes and the number of vertices.
    It makes sure that a path exists between peers. It returns an object of two elements, edges and node. Edges
    is an array of tuple of nodes, and node is an array of node elements. The final connected adjacency list is stored in bazaar.json
    Args:
        node: number of peers
        vertices: max number of edges in the graph
    Returns:
        Graph: {Edge: [()], node:[]}
    """
    while True:
        d = defaultdict(list)
        # Generate
        G = nx.gnm_random_graph(node,vertices)
        edges = G.edges
        # Making sure that the graph is connected
        if not nx.is_connected(G):
            continue
        for key,value in edges:
            d[key].append(value)
            d[value].append(key)
        is_found = False
        # Check for neighbours not exceeding 
        for _, values in d.items():
            if len(values)>3:
                is_found = True
                break
        if is_found:
            continue
        return G


def create_bazar(peer_list, show_graph=True):
    """
    This function converts the graph generated by the generate graph function to the required bazaar
    format of buyers and sellers. It creates an adjacency list and stores it in a json file.
    Args:
        peer_list [] : list of peer ids 
    Returns:
        Edges [()] : array of connected edges 
    """
    G = generate_graph(len(peer_list),len(peer_list)+2)
    edges = G.edges
    pos_dict = {}
    for i, peer in enumerate(peer_list):
        pos_dict[i] = peer
    nx.draw_networkx(G,labels = pos_dict,with_labels=True,node_color="red")
    print("Showing the graphical representation of the bazaar")
    # Start the plt.show as a seperate thread so that application can proceed to run
    if show_graph: 
        plt.show(block=False)
        plt.pause(5)
    adj_list = defaultdict(list)
    for peer_1,peer_2 in edges:
        adj_list[pos_dict[peer_1]].append(pos_dict[peer_2])
        adj_list[pos_dict[peer_2]].append(pos_dict[peer_1])
    
    json_object = json.dumps(adj_list)
    with open("bazaar.json", "w") as outfile:
        outfile.write(json_object)
    return G.edges


def get_longest_path(d):
    """
    This function takes in as arguments a nxn matrix, where n is the nuber of peers.
    Every row and column represent a peer and the value corresponding to that row and 
    column is whether a connection is present between those 2 peers.
    Here longest path is the path with maximum among all pair of nodes.
    Args:
        d: nxn matrix
    Returns:
        longest path in the graph: int
    """
    N = len(d)
    NBITS = 1 << N

    m = [[-2 for j in range(NBITS)] for i in range(N)]
    p = [[-2 for j in range(NBITS)] for i in range(N)]

    def subsolve(b, visited):
        if (visited == (1 << b)):
            p[b][visited] = -1
            return 0

        if (m[b][visited] == -2):
            best = -1
            bestPred = -1
            for i in range(N):
                if (i != b and ((visited >> i) & 1) and d[i][b] != -1):
                    x = subsolve(i, visited & ~(1 << b))
                    if (x != -1):
                        x += d[i][b]
                        if (x > best):
                            best = x
                            bestPred = i  
            m[b][visited] = best
            p[b][visited] = bestPred
        return m[b][visited]


    def solve():
        best = -1
        for b in range(N):
            x = subsolve(b, (1 << N) - 1)
            if (x > best):
                best = x
        return best
    return solve()


def get_hop_count(edges):
    """
    This function gets the max hop count for the network. it uses a matrix of connection mapping
    between peers. Each row is peer and each column is a peer. 0 represents no connection, 1 represents
    connection is present between those 2 peers. It returns an integer which is used as the hopcount for
    all the peers (length of longest path-1). Due to time constraints, for nodes greater than 10, this 
    function doesn't compute the longest path instead just returns the hop count as 6.
    Args:
        edges: nxn matrix
    Returns:
        hopcount: int
    """
    try:
        f = open("bazaar.json")
    except Exception as e:
        print(f"Something went wrong while reading bazar.json file!!! Make sure that the peer to peer network has been constructed")
    data = json.load(f)

    # Converting adjecency list to binary matrix form

    nodes = 0
    for key, _ in data.items():
        nodes+=1
    graph_matrix = [[0]*nodes for _ in range(nodes)]
    if nodes == 2:
        return 1
    if nodes>10:
        return 6
    for e in edges:
        graph_matrix[e[0]][e[1]] = 1
    return get_longest_path(graph_matrix)-1



