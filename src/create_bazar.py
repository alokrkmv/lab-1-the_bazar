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
    plt.show(block=False)
    print("Showing the graphical representation of the bazaar")
    plt.pause(8)
    adj_list = defaultdict(list)
    for peer_1,peer_2 in edges:
        adj_list[pos_dict[peer_1]].append(pos_dict[peer_2])
        adj_list[pos_dict[peer_2]].append(pos_dict[peer_1])
    
    json_object = json.dumps(adj_list)
    with open("bazaar.json", "w") as outfile:
        outfile.write(json_object)