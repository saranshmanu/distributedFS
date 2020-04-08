from src.server import server_init
from src.utils.ipfs import connect_ipfs
from dotenv import load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)

if connect_ipfs():
    server_init()