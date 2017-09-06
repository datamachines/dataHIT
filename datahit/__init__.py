import os
#from flask_sse import sse
from elasticsearch import Elasticsearch
from datetime import datetime

def init(config, app):
    if not os.path.exists(config['datadir']):
      os.makedirs(config['datadir'])
