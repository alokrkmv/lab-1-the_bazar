import Pyro5.api
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Lock
import random
import time
import json

class Peer(Thread):
    def __init__(self,id,role,items, items_count,host):

        # To inherit the thread class it is necessary to inherit the init and 
        # run method of the thread class
        Thread.__init__(self)
        self.id = id
        self.role  = role
        self.items = items
        self.output = "tmp/output.txt"
        self.items_count = items_count
        self.item = items[random.randint(0, len(items) - 1)]
        self.executor = ThreadPoolExecutor(max_workers=20)
        self.host  = host
        self.hope_count = 4
        self.neighbors = {}
        

    def __str__(self):
        return f'id : {self.id},role : {self.role},nameserver: {self.name_server},items: {self.items})'

    @Pyro5.api.expose
    def ping(self):
        # print("Pong")
        return "Pong"
    
    def get_nameserver(self):
        return Pyro5.api.locate_ns(host=self.host)
    

    def set_healthy_neighbors(self, peer_id):
        time.sleep(2)
        bazar_network = open("bazaar.json")
        data = json.load(bazar_network)
        try:
            expected_neighbors = data[peer_id]
        except Exception as e:
            print("Loading neighbors for bazaar failed with error {e} Please make sure that the bazar has been created properly")
        for neighbor in expected_neighbors:
         
            neighbor_uri = self.get_nameserver().lookup(neighbor)
        
            self.neighbors[neighbor] = neighbor_uri
               
            
    # Inheriting the run method of thread class
    def run(self):
        try:
            # Registering the peer as Pyro5 object
            with Pyro5.api.Daemon(host = self.host) as daemon:
                try:
                    peer_uri = daemon.register(self)
                    self.get_nameserver().register(self.id,peer_uri)
                except Exception as e:
                    print(f"Registring to nameserver failed with error {e}")
                if self.role == "buyer":
                    print(f"{self.id} joined the bazar as buyer looking for {self.item} at {time.time()}")
                else:
                    print(f"{self.id} joined the bazar as seller selling {self.item} at {time.time()}")
                
                # Start the Pyro requestLoop
                self.executor.submit(daemon.requestLoop)

                # Check that all neighbours are healthy before starting buy or sell
                # t1 = Thread(target = self.set_healthy_neighbors,kwargs={"peer_id":self.id})
              
                self.set_healthy_neighbors(self.id)
                for _,uri in self.neighbors.items():
                    proxy = Pyro5.api.Proxy(uri)
                    print(proxy.ping())
                    
        
        except Exception as e:
            pass



        