import os
from dotenv import load_dotenv
load_dotenv()

val=os.getenv('MONGO')

import pymongo
CLIENT = pymongo.MongoClient(val)