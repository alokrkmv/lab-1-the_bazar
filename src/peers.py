from threading import Thread, Lock
import random

class Peer(Thread):
    def __init__(self, id, role, name_server, items, items_count):

        # To inherit the thread class it is necessary to inherit the init and 
        # run method of the thread class
        Thread.__init__(self)
        self.id = id
        self.role  = role
        self.name_server = name_server
        self.items = items # list
        self.output = "tmp/output.txt"
        self.items_count = items_count
        self.max_items = items_count
        self.item = items[random.randint(0, len(items) - 1)]
        self.neighbours = []
        self.sellers = []

    def __str__(self):
        return f'id : {self.id},role : {self.role},nameserver: {self.name_server},items: {self.items})'

    def lookup(self, buyerID: str, product_name: str, hop_count: int, search_path: [str]):
        """
        Parameters
        ----------
        buyerID: str
            id of the buyer that sent the request
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

        if self.role == "seller" and product_name == self.item:
            # If seller found and selling the item call reply
            self.reply(self.id, search_path)
        else:
            # Else do something
            # find neighbours 
            neighbours = self.get_neighbours(self.id)

            # if the serach_path is not empty, take the previous peer from which the request was received
            if search_path: 
                previous_peer = search_path[-1]
            else:
                previous_peer = None
            
            # For each neighbour
            for each_neighbour in neighbours:
                # create a deep copy of the search path
                new_search_path = search_path[:]
                if previous_peer and each_neighbour == previous_peer:  # for search path empty
                    continue
                ######### lookup function of the next peer with peer id each_neighbour ###############
                lookup(buyerID, product_name, hop_count, new_search_path.append(self.id))

        return 

    def get_neighbours(self, id):
        # Returns the neighbours of the current peer
        pass

    def reply(self, seller_id: str, reply_path: [str]):
        # 
        if reply_path:
            previous_peer = reply_path.pop()
            # call the reply of previous_peer
            reply(seller_id, reply_path)

        else: # empty reply_path means, you reply has reached the buyer, add the seller_id to the list
            # this line appends the seller ids of all the peers from which the buyr got a reply
            self.sellers.append(seller_id)


    def buy(self):
        if self.items_count > 0:
            self.items_count -= 1
            return True
        else:
            new_list_of_items = self.items[:]
            new_list_of_items.remove(self.item)
            self.item = new_list_of_items[random.randint(0, len(new_list_of_items) - 1)]
            self.items_count = self.max_items
            print("Seller id {} is now the seller of {}.".format(self.id, self.item))
            return False
