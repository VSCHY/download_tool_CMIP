#!/usr/local/bin/python
#
from pyesgf.search import SearchConnection
from pyesgf.logon import LogonManager
import numpy as np
import json
import configparser
from module_function import get_sid, get_member
#
config=configparser.ConfigParser()
config.read("config.def")
openid=config.get("OverAll", "openid")
password=config.get("OverAll", "password")
#
##################
#
# PARAMETERS 
#
# json output file
dfile  = "./Models_CMIP6.json"
# experiments
Lexp_id = ['historical', "ssp585"]
# variables
Lvar = ["tasmax", "tasmin", "pr"]

##################
#
# CONNECTION
#
lm = LogonManager()
lm.logoff()
lm.logon_with_openid(openid, password = password, bootstrap = True)
t = "http://esgf-node.llnl.gov/esg-search"
print("connect")
conn = SearchConnection(t, distrib=True)
#
# Get the different source_id (model)
#
Lsid = get_sid(conn, exp_id = "ssp585", variable = "tasmax")
#
# For each source_id, save in D the members with the required data
#
D = {}
for i, sid in enumerate(Lsid):
    if sid not in D:
       print(sid, i, "/", len(Lsid))
       L = get_member(conn, sid, Lexp_id, Lvar)
       if len(L)> 0:
           D[sid] = L
           print(len(L), "simulations")

with open(dfile, "w") as a_file:
    json.dump(D, a_file)

    
