from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ROOT_DIR = getenv("ROOT_DIR", "./data")
