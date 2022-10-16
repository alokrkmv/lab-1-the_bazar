import json
from logging import exception
import os
import sys
import random

import Pyro5.api

from peers import Peer
from create_bazar import create_bazar
# This is the main process which takes command line argument
# It is responsible for spwaning peers as buyers or sellers

def main():
    config_file = open(os.path.join(os.path.dirname(__file__), '..', 'config.json'))
    data = json.load(config_file)
    default_configs = data["default_config"]
    # If number of peers is passed through command line then use that as number of peer
    # otherwise pick default number of peers from config file
    if len(sys.argv)==3:
        number_of_peers = int(sys.argv[2])
    else:
        number_of_peers = default_configs["number_of_peers"]
    roles = default_configs["roles"]
    items = default_configs["items"]
    items_count = default_configs["number_of_items"]
    peers = []
    # Locate the nameserver currently running on the system
    try:
        nameserver = Pyro5.api.locate_ns()
    except exception as e:
        print(f"Locating nameserver failed with exception {e}")
    # Make sure that there is at least one buyer and one seller in the network
    ids = {}
    for i,r in enumerate(roles):
        id = f"{r}{str(i)}"
        ids[id] = r

    for i in range(2,number_of_peers):
        role = roles[random.randint(0,len(roles)-1)]
        id = f"{role}{str(i)}"
        ids[id] = role
    for id,role in ids.items():
        peer = Peer(id,role,nameserver,items,items_count)
        peers.append(peer)
    return peers

        


if __name__=='__main__':
    peers = main()
    peer_id_list = []
    for peer in peers:
        peer_id_list.append(peer.id)
    create_bazar(peer_id_list)
    
