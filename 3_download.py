#!/usr/local/bin/python
#
import numpy as np
import json
import subprocess
from module_function import loadjson, get_script, setdirectory
from os import path
import os
import configparser
config=configparser.ConfigParser()
config.read("config.def")
openid=config.get("OverAll", "openid")
password=config.get("OverAll", "password")
# 
###################
lm = LogonManager()
lm.logoff()

def log_to_esgf():
    lm.logon_with_openid(openid, password = password, bootstrap = True)
    t = "http://esgf-node.llnl.gov/esg-search"
    conn = SearchConnection(t, distrib=True)

log_to_esgf()
#
##################
#
# PARAMETERS
#
wrkdir = "/datoshildr/CMIP6"
dfile = "Models_CMIP6.json"
test = False
#
##################
#
a = loadjson(dfile, test)

for sid in list(a.keys()):
    print("**", sid, "**")
    dire = wrkdir+"/"+sid
    # Start with orog
    try:
        os.chdir(dire)
        subprocess.check_call(["bash", "script.bash"])
    except:
        print("NO OROG")
        with open(wrkdir + "/out.log", "a") as f:
            f.write("source_id: {0} has no orog variable\n".format(sid))
        continue

    # Then other variables (only if orog exists)
    if path.exists(dire+"/script.bash"):
        for member in a[sid]:
            print(member)
            # Ceate directory with member if not exists (function)
            mdire = dire+"/"+member
            for expid in ["ssp585", "historical"]:
                expdire = mdire +"/"+expid
                for var in ["tasmax", "tasmin","pr"]:
                    vdire = expdire+"/"+var
                    os.chdir(vdire)
                    print(sid, member, expid, var)
                    if not lm.is_logged_on(): log_to_esgf()
                    try:
                       subprocess.check_call(["bash", "script.bash"])
                    except:
                       with open(wrkdir + "/out.log", "a") as f:
                           f.write("Issue with downloading file:\n")
                           f.write("source_id: {0}, member: {1},experimental_id: {2}, variable: {3}\n".format(sid, member, expid, var))

# Possibility to handle launch of script and concatenation with SUBPROCESS
# But download speed seemed lower, is it due to SUBPROCESS ?         

