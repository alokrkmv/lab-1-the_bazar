import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import json

# Creating the connected peer to peer network. The final connected adjacency list is stored in bazaar.json

def generate_graph(node, vertices):
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
def create_bazar(peer_list):
    G = generate_graph(len(peer_list),len(peer_list)+2)
    edges = G.edges
    pos_dict = {}
    for i, peer in enumerate(peer_list):
        pos_dict[i] = peer
    nx.draw_networkx(G,labels = pos_dict,with_labels=True,node_color="red")
    print("Showing the graphical representation of the bazaar")
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



# d = [
# [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
# [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
# [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
# [0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
# [0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
# [0, 0, 0 ,0 ,1, 0, 1, 1, 0, 0],
# [0, 0, 0 ,0 ,1, 1, 0, 1, 0, 0],
# [0, 0, 0 ,0, 0, 1, 1, 0, 1, 0],
# [0, 0, 0 ,0, 0, 0, 0, 1, 0, 1],
# [0, 0, 0 ,0, 0, 0, 0, 0, 1, 0],
# ]

# d = [
#     [0, 1, 0, 0, 0, 1],
#     [1, 0, 1, 0, 0, 0],
#     [0, 1, 0, 1, 1, 0],
#     [0, 0, 1, 0, 1, 0],
#     [0, 0, 1, 1, 0, 1],
#     [1, 0, 0, 0, 1, 0]
# ]

# d = [
#     [0, 1, 0, 0, 1],
#     [1, 0, 1, 0, 0],
#     [0, 1, 0, 1, 0],
#     [0, 0, 1, 0, 1],
#     [1, 0, 0, 1, 0],
# ]

# This method finds the length of longest path in a graph
# Here longest path is the path with maximum among all pair of nodes
def get_longest_path(d):
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

# This function sets hop count for the bazar (length of longest path-1)
def get_hope_count(edges):
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
    for e in edges:
        graph_matrix[e[0]][e[1]] = 1
    return get_longest_path(graph_matrix)-1



