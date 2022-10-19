import Pyro4
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Lock
import random
import time
import json
import copy


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
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.host  = host
        self.hop_count = 4
        self.neighbors = {}
        self.lock_item = Lock()
        self.lock_sellers = Lock()
        self.output_array = []
        self.max_items = 10
        self.sellers = []
        

    def __str__(self):
        return f'id : {self.id},role : {self.role},nameserver: {self.name_server},items: {self.items})'

    @Pyro4.expose
    def ping(self):
        return "Pong"
    
    def get_nameserver(self):
        return Pyro4.locateNS(host=self.host)
    

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
            with Pyro4.Daemon(host = self.host) as daemon:
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
          
           
                while True and self.role=="buyer":
                    lookups = []
                    
                    for neighbor,uri in self.neighbors.items():
                    
                        
                        neighbor_proxy = Pyro4.Proxy(uri)
                        print(f"Buyer {self.id} issues lookup to {neighbor} at time {time.time()}")
                        id_list = [self.id]
                        lookups.append(self.executor.submit(neighbor_proxy.lookup,self.item,self.hop_count,id_list))
                    for lookup_request in lookups:
                        lookup_request.result()
                    
                    with self.lock_sellers:
                        if self.sellers:
                            random_seller_id = self.sellers[random.randint(0, len(self.sellers) - 1)]

                            seller = Pyro4.Proxy(self.get_nameserver().lookup(random_seller_id))
                            picked_seller = self.executor.submit(seller.buy,self.id)

                            if picked_seller.result():
                                print(time.time(), self.id, "bought", self.item, "from", random_seller_id)
                            else:
                                print(time.time(), self.id, "failed to buy", self.item, "from", random_seller_id)
                        self.sellers = []
                        self.item = self.items[random.randint(0, len(self.items) - 1)]
                        print(f"Buyer {self.id} now picked item {self.item} to buy at time {time.time()}")
                    time.sleep(1)
                
                while True:
                    time.sleep(1) 
        
        except Exception as e:
            print(f"Something went wrong in run method with exception {e}")
    
    # This method is reponsible for the purchase of an item item logic
    @Pyro4.expose
    def buy(self, buyer_id):
        # with self.lock_item:
        if self.items_count > 0:
            self.items_count -= 1
            print(f"{buyer_id} purchase item {self.item} from seller {self.id} at {time.time()}")
            print(f"Seller {self.id} now has {self.items_count} remaining for item {self.item}")
            return True
        else:
            while True:
                picked_item = self.items[random.randint(0, len(self.item) - 1)]
                if self.item!=picked_item:
                    self.item = picked_item
                    break
                    
                self.items_count = self.max_items
                print("Seller id {} is now the seller of {}.".format(self.id, self.item))
                self.output_array.append(f"Seller {self.id} is now the seller of {self.item}.")
                return False

    # This  method is the lookup method which transmits the call to its neighbours
    # until a suitable seller for the item is found
    @Pyro4.expose
    def lookup(self,product_name: str, hop_count: int, search_path):
        """
        Parameters
        ----------
        product_name: str
            product demanded by the buyer
        hop_count: int
            number of hops remaining after the previous hop
        search_path: [str]
            list of ids of the peers via which the request arrived
        Return
        ------
        Null
        """
        
        if hop_count < 1:
            return
        else:
            hop_count -= 1
        previous_peer = search_path[-1]
        try:
            if self.role == "seller" and product_name == self.item:
                # If seller found and selling the item call reply
                recipient = Pyro4.Proxy(self.get_nameserver().lookup(previous_peer))
                search_path.pop()
                search_path.insert(0,self.id)
                self.executor.submit(recipient.reply,self.id,search_path)
            else:
                # For each neighbour
                for each_neighbour,uri in self.neighbors.items():
                    # create a deep copy of the search path
                    new_search_path = search_path[:]
                    if each_neighbour == previous_peer:  
                        continue
                    neighbor_proxy = Pyro4.Proxy(uri)
                    if self.id not in search_path:
                        new_search_path.append(self.id)
                    self.executor.submit(neighbor_proxy.lookup,product_name,hop_count,search_path)
                    ######### lookup function of the next peer with peer id each_neighbour ###############
                
        except Exception as e:
            print(f"Something went wrong in lookup with exception {e}")


    @Pyro4.expose
    def reply(self, seller_id: str, id_list):
        try:
            if id_list and len(id_list) == 1:

                print(time.time(), self.id, "got a match reply from", id_list[0])

                with self.lock_sellers:
                    self.sellers.append(id_list[0])

            elif id_list and len(id_list) > 1:
                recipient_id = id_list.pop()
                with Pyro4.Proxy(self.neighbors[recipient_id]) as recipient:
                    self.executor.submit(recipient.reply, self.id, id_list)

        except(Exception) as e:
            print(f"Something went wrong while trying to fecth the reply with error {e}")

        



        