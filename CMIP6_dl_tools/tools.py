"""
Tools for CMIP6 output download.
"""

import numpy as np
import os
from os import path
import json
import sys


def get_sid(conn, exp_id, variable):
    """
    Get the list of models with the experiments 'exp_id' and the variable 'variable'.
    This is used as a basis to perform the following search.
    
    Parameters:
    -----------
    conn (Connection object)
    exp_id (str): experiment name
    variables (str): variable name
    
    Returns:
    --------
    Lsid (list of str): List of models available
    
    ----------------------------------------------------
    """
    ctx = conn.new_context(project="CMIP6", frequency='mon', experiment_id=exp_id, \
                           variable = variable, realm = "atmos", facets = "*")
    source_id = []
    a = ctx.search()
    source_id = [b.json["source_id"] for b in a]

    Lsid = np.unique(source_id)
    return Lsid 



def get_member(conn, sid, Lexp_id, Lvar):
    """
    Get the list of member from a model (sid) for the different 
        experiments abnd variables specified.
    
    Parameters:
    -----------
    conn (Connection object)
    sid (str): name of the model
    Lexp_id (list of str): list of experiments
    Lvar (list of str): list of variables
    
    Returns:
    --------
    Lmember (list of str): list of member 
    
    ----------------------------------------------------
    """
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

    Lmember = []
    for v in variant:
       if np.sum(D[v]) == nexp*nvar:
          Lmember.append(v)
    Lmember = list(np.unique(L))

    return Lmember



def setdirectory(directory):
    """
    Create a directory if not existing.
    
    Parameters:
    -----------
    directory (str): directory to create if not existing
    
    ----------------------------------------------------
    """
    if not path.exists(directory) : 
        os.mkdir(directory)


        
def get_script(conn, sid, expid = None, var = None, member = None, realm = "atmos"):
    """
    Get the download script for a variable ('var') of a member ('member') 
        from the experiment 'expid' from the model 'sid'.
    
    Parameters:
    -----------
    conn (Connection object)
    sid (str): model
    expid (str): experiment
    var (str): variable
    member (str): member of the model
    realm (str): component of the model
    
    Returns:
    --------
    script (str): download script
    
    ----------------------------------------------------
    """
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



def script_subfunction(search, i):
    """
    Subfunction to get the script for get_script function.
    It checks the element i within the search object 
            and see if it finds a script available.
    
    Parameters:
    -----------
    search (Search object)
    i (int): index within the search object to look at
    
    Returns:
    --------
    script (str): download script if found
    
    ----------------------------------------------------
    """
    try:
        simu = search[i]
    except:
        print("source_id: {0}, experiment_id: {1}, variables: {2}, realm: {3}, variant_label: {4}".format(sid, expid, var, ream, member))
        sys.exit()
    fc = simu.file_context()
    script = fc.get_download_script()
    if script == "No files were found that matched the query": script = None
    return script



def loadjson(dfile, testmode = False):
    """
    Load the json with available model/member. 
    
    Parameters:
    -----------
    dfile (str): directory of the json file
    testmode (bool): test mode
    
    Returns:
    --------
    out (str): dictionnary of available model/member
    
    ----------------------------------------------------
    """
    out = json.load(open(dfile,"r"))
    if testmode:
        models = list(out.keys())
        b = {}
        b[models[0]] = [out[models[0]][0]]
        out = b
    return out
#
def savejson(dfile,D):
    with open(dfile, "w") as a_file:
        json.dump(D, a_file)

def save_script(script, directory, filename):
    with open(directory + "/" + filename, "w") as f:
                f.write(script)

            
########################


def get_url( sid, expid = None, var = None, member = None, realm = "atmos"):
    """
    (IN TEST)
    
    Experiment to get directly the urls for a specific simulation.
    (the idea is to perform directly a wget)
    
    Parameters:
    -----------
    sid (str): model
    expid (str): experiment
    var (str): variable
    member (str): member of the model simulations
    realm (str): component 
    
    Returns:
    --------
    urls (list of str): list of urls
    
    ----------------------------------------------------
    """
    from pyesgf.search import SearchConnection
    conn = SearchConnection('http://esgf-data.dkrz.de/esg-search', distrib=False)
    ctx = conn.new_context(project="CMIP6", frequency='mon', source_id = sid, experiment_id=expid, variable = var, variant_label = member, facets = "*")
    ds = ctx.search()[0]
    files = ds.file_context().search()
    urls = [f.download_url for f in files]
    return urls
