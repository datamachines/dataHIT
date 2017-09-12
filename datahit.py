#!/usr/bin/python
# Probably belongs here...
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import datahit
from datahit import datahithtml, datahitlog
import json
from elasticsearch import Elasticsearch
import yaml
import sys

app = Flask(__name__, static_url_path='')
rundate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# TODO: Make config file a command line option
config = yaml.safe_load(open("config.yaml"))
app = Flask(__name__)
# TODO: Make ES information configurable in config file
eshost = config['eshost']
esport = int(config['esport'])
esindex = config['esindex']
esdoc_type = "datarec"

es = Elasticsearch([{'host': eshost, 'port': esport}])
datahitlog.log("Connected to Elasticsearch")
esMappings = {
    "mappings" : {
        esdoc_type : {
            "properties" : {
                "userID" : {
                    "type" : "string",
                    "index" : "not_analyzed"
                },
                "recID" : {
                    "type" : "string",
                    "index" : "not_analyzed"
                }
            }
        }
    }
}
res = es.indices.create(index=esindex, ignore=400, body=esMappings)

# For development until/when auth is implemented
userID = "869b0838-b103-4b79-bc02-d9ea6a9d6710" # this is a random guid

@app.route("/editor", methods=["POST","GET"])
def datahiteditor():
    recID = request.form['recID']
    datarec = {}
    query = {"query": { "ids" : { "type" : "datarec", "values" : [recID] }}}
    r = es.search(index=esindex, body=query)
    hitsTotal = int(r['hits']['total'])
    if hitsTotal == 0:
        with open('static/schemas/default.json') as f:
            datarec = json.loads(f.read())
        datahitlog.log("Loading default record data.")
    elif hitsTotal == 1:
        datarec = r['hits']['hits'][0]['_source']['datarec']
        datahitlog.log("Loading data record " + recID)
    values = {
        'date': rundate,
        'recID': recID,
        'datarec': json.dumps(datarec)
        }
    return datahithtml.render("templates/editor.html", values, config['cacheJavascript'])

@app.route("/list")
def hitlist():
    query = {
        "query" : {
            "constant_score" : {
                "filter" : {
                    "term" : {
                        "userID" : userID
                    }
                }
            }
        }
    }
    print(json.dumps(query))
    r = es.search(index=esindex, doc_type=esdoc_type, body=query)
    recTable = datahithtml.createRecTable(r['hits']['hits'])
    values = {'recTable': recTable }
    return datahithtml.render("templates/list.html", values, config['cacheJavascript'])

@app.route("/saverec", methods=["POST"])
def saveplan():
    recDoc = request.get_json()
    recDoc['userID'] = userID
    res = es.index(index=esindex, doc_type=esdoc_type, id=recDoc['recID'], body=recDoc)
    print(json.dumps(res))
    return "Record saved!"

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=config['port'],threaded=True)
