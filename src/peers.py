from threading import Thread, Lock
import random

class Peer(Thread):
    def __init__(self,id,role,name_server,items, items_count):

        # To inherit the thread class it is necessary to inherit the init and 
        # run method of the thread class
        Thread.__init__(self)
        self.id = id
        self.role  = role
        self.name_server = name_server
        self.items = items
        self.output = "tmp/output.txt"
        self.items_count = items_count
        self.item = items[random.randint(0, len(items) - 1)]

    def __str__(self):
        return f'id : {self.id},role : {self.role},nameserver: {self.name_server},items: {self.items})'

        