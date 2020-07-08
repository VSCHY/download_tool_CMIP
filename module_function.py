#!/usr/local/bin/python
#
import numpy as np
from os import path
import json
#
def get_sid(conn, exp_id, variable):
    # all historical with tmax (to reduce the list)
    ctx = conn.new_context(project="CMIP6", frequency='mon', experiment_id='ssp585', variable = "tasmax", realm = "atmos")
    source_id = []
    a = ctx.search()
    source_id = [b.json["source_id"] for b in a]

    Lsid = np.unique(source_id)
    return Lsid 
#
def get_member(conn, sid, Lexp_id, Lvar):
    # Find the different members
    ctx = conn.new_context(project="CMIP6", source_id = sid, frequency='mon', experiment_id=Lexp_id, variable = Lvar, realm = "atmos")
    a = ctx.search()
    
    lenv = [len(b.json["variant_label"]) for b in a]
    variant = [b.json["variant_label"][0] for b in a]
    D = {}
    for v in variant:
       D[v] = [0,0,0,0,0,0]
    for b in a:
       member = b.json["variant_label"][0]
       var = b.json["variable"][0]
       expid = b.json["experiment_id"][0]
       expf = 0
       if expid == "ssp585":
          expf = 1
       if var == "tasmax": 
          nvar = 0
       elif var == "tasmin":
          nvar = 1
       elif var == "pr":
          nvar = 2

       D[member][3*expf+nvar] = 1

    L = []
    for v in variant:
       if np.sum(D[v]) == 6:
          L.append(v)
    L = list(np.unique(L))

    return L
#
def setdirectory(directory):
    if not path.exists(directory) : 
        os.mkdir(directory)
#
def get_script(conn, sid, member, expid, var):
    ctx = conn.new_context(project="CMIP6", frequency='mon', source_id = sid, experiment_id=expid, variable = var, realm = "atmos", variant_label = member)
    search = ctx.search()
    simu = search[0]
    fc = simu.file_context()
    script = fc.get_download_script()
    return script
#
def loadjson(dfile, testmode = False):
    a = json.load(open(dfile,"r"))
    if testmode:
        models = list(a.keys())
        b = {}
        b[models[0]] = [a[models[0]][0]]
        a = b
    return a
#


