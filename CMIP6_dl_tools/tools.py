#!/usr/local/bin/python
#
import numpy as np
import os
from os import path
import json
import sys
#
def get_sid(conn, exp_id, variable):
    # all historical with tmax (to reduce the list)
    ctx = conn.new_context(project="CMIP6", frequency='mon', experiment_id='ssp585', variable = "tasmax", realm = "atmos", facets = "*")
    source_id = []
    a = ctx.search()
    source_id = [b.json["source_id"] for b in a]

    Lsid = np.unique(source_id)
    return Lsid 
#
def get_member(conn, sid, Lexp_id, Lvar):
    # Find the different members
    ctx = conn.new_context(project="CMIP6", source_id = sid, frequency='mon', experiment_id=Lexp_id, variable = Lvar, facets = "*")
    a = ctx.search()
    
    variant = [b.json["variant_label"][0] for b in a]
    nexp = len(Lexp_id)
    nvar = len(Lvar)
    EXP = {Lexp_id[i]:i for i in range(nexp)}
    VAR = {Lvar[i]:i for i in range(nvar)}
    
    # A améliorer : Développement plus général
    # Ajouter condition orog
    D = {}
    for v in variant:
       D[v] = [0]*(nexp*nvar)
    for b in a:
       member = b.json["variant_label"][0]
       var = b.json["variable"][0]
       expid = b.json["experiment_id"][0]
       expf = EXP[expid]
       varf = VAR[var]

       D[member][nvar*expf+varf] = 1

    L = []
    for v in variant:
       if np.sum(D[v]) == nexp*nvar:
          L.append(v)
    L = list(np.unique(L))

    return L
#
def setdirectory(directory):
    if not path.exists(directory) : 
        os.mkdir(directory)
#



#
def get_script(conn, sid, expid = None, var = None, member = None, realm = "atmos"):
    if var == "orog":
        ctx = conn.new_context(project="CMIP6", source_id = sid, variable = var, facets = f"{sid},{var}")
    else:
        ctx = conn.new_context(project="CMIP6", frequency='mon', source_id = sid, experiment_id=expid, variable = var, variant_label = member, facets = "*")
    search = ctx.search()

    script = None
    i=0
    while i<len(search) and script is None:
        script = script_subfunction(search, i)
        i +=1
    if script is None: script = "No files were found that matched the query"

    return script
#
def script_subfunction(search, i):
    try:
        simu = search[i]
    except:
        print("source_id: {0}, experiment_id: {1}, variables: {2}, realm: {3}, variant_label: {4}".format(sid, expid, var, ream, member))
        sys.exit()
    fc = simu.file_context()
    script = fc.get_download_script()
    if script == "No files were found that matched the query": script = None
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
def savejson(dfile,D):
    with open(dfile, "w") as a_file:
        json.dump(D, a_file)

def save_script(script, directory, filename):
    with open(directory + "/" + filename, "w") as f:
                f.write(script)


########################

def get_url( sid, expid = None, var = None, member = None, realm = "atmos"):
    from pyesgf.search import SearchConnection
    conn = SearchConnection('http://esgf-data.dkrz.de/esg-search', distrib=False)
    ctx = conn.new_context(project="CMIP6", frequency='mon', source_id = sid, experiment_id=expid, variable = var, variant_label = member, facets = "*")
    ds = ctx.search()[0]
    files = ds.file_context().search()
    url = [f.download_url for f in files]
    return url