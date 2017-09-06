import string
import os
import glob
import uuid
from .datahitlog import log

def render(filename, values, cacheJavascript = True):
  values['dev'] = ""
  if cacheJavascript is False:
    values['dev'] = "?scriptver=" + randScriptVer()
    log("Warning! Not caching javascript. Use this setting for development only. Check config.yaml","WARN")
  with open(filename) as f:
    template = f.read()
  t = string.Template(template)
  h = t.substitute(values)
  return h

def dirListBasenames(dirPathPattern):
    names = [os.path.basename(x) for x in glob.glob(dirPathPattern)]
    return names

def randScriptVer():
    return str(uuid.uuid4())

def createPlanTable(hits):
    tablerows = []
    for hit in hits:
        planDoc = hit['_source']
        namecell = "<td>" + planDoc['plan']['name'] + "</td>"
        actioncell = "<td><form action='/editor' method='POST' id='form" + planDoc['planID'] + "'>\n" + \
                    "<input type='hidden' name='planID' value='" + planDoc['planID'] + "'></form>\n" + \
                    "<button type='submit' form='form" + planDoc['planID'] + "' id='button" + planDoc['planID'] + "' class='tiny'>Open</button></td>\n"
        tablerows.append("<tr>" +  namecell + actioncell + "</tr>")
    return "\n".join(tablerows)
