import ipfsapi

# connect to the IPFS network
def connect_ipfs():
    try:
        api = ipfsapi.connect('127.0.0.1', 5001)
        return True
    except ipfsapi.exceptions.ConnectionError as ce:
        print('Error: ', str(ce))
        return False

# get the IPFS connection variable
def get_ipfs_connection():
    return ipfsapi.connect('127.0.0.1', 5001)

def get_ipfs_config():
    api = get_ipfs_connection()
    return api.id()

# add file to the IPFS network
def add_file(name):
    api = get_ipfs_connection()
    try:
        new_file = api.add(name)
        return new_file, True
    except ipfsapi.exceptions.ConnectionError as ce:
        return None, False
