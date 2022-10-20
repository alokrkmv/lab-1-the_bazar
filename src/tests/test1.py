import os
# from . import create_bazar #.create_bazar as create_bazar
from create_bazar import get_hop_count, create_bazar
from peers import Peer


ids = {
    "buyer0": "buyer",
    "seller1": "seller"
}

items = ["fish","salt","boar"]
items_count = 5
hostname = "localhost"
base_path = os.getcwd()
peers = []
for id, role in ids.items():
    peer = Peer(id, role, items, items_count, hostname, base_path)
    peers.append(peer)

# print(peers)
peer_id_list = []
for peer in peers:
    peer_id_list.append(peer.id)
edges = create_bazar(peer_id_list)
hop_count = get_hop_count(edges)

for peer in peers:
    peer.hop_count = 2

    if peer.role == "buyer":
        peer.item = ["fish","salt","boar"][1]

    if peer.role == "seller":
        peer.item = ["fish","salt","boar"][1]
    print(peer.role, peer.item)

for peer in peers:
    peer.start()
    
