import Pyro5.api
import sys
def start_nameserver():
    arguments = sys.argv
    host = ""
    try:
        host = arguments[1]
    except Exception as e:
        print("Host not provided for namespace server to start!!!")

    try:
        # Check if the nameserver is already running
        nameserver = Pyro5.api.locate_ns(host=host)
        print(f"Namespace server is already running on {host}")
    except Exception as e:
        print("No nameserver found!!! Starting a new server on the host machine")
        Pyro5.nameserver.start_ns_loop(host=host)

if __name__=='__main__':
    start_nameserver()


