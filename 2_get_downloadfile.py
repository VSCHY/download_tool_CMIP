#!/usr/local/bin/python
#
from pyesgf.search import SearchConnection
from pyesgf.logon import LogonManager
import numpy as np
import json
import subprocess
from module_function import loadjson, get_script, setdirectory
from os import path
import configparser
config=configparser.ConfigParser()
config.read("config.def")
openid=config.get("OverAll", "openid")
password=config.get("OverAll", "password")
# 
###################

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
# CONNECTION
#
lm = LogonManager()
lm.logoff()
lm.logon_with_openid(openid, password = password, bootstrap = True)
t = "http://esgf-node.llnl.gov/esg-search"
print("connect")
conn = SearchConnection(t, distrib=True)

a = loadjson(dfile, test)

for sid in list(a.keys()):
    print("**", sid, "**")
    dire = wrkdir+"/"+sid
    setdirectory(dire)
    # Start with orog
    if not path.exists(dire+"/script.bash"):
        try:
            script = get_script(conn, sid = sid, var = "orog", realm = "land")
            with open(dire + "/script.bash", "w") as f:
                f.write(script)
        except:
            with open(dire + "/OROG_ABSENT", "w") as f:
                f.write("The variable 'orog' is not available")
            print("NO OROG")
            continue

    # Then other variables (only if orog exists)
    if path.exists(dire+"/script.bash"):
        for member in a[sid]:
            print(member)
            # Ceate directory with member if not exists (function)
            mdire = dire+"/"+member
            setdirectory(mdire)
            for expid in ["ssp585", "historical"]:
                expdire = mdire +"/"+expid
                setdirectory(expdire)
                for var in ["tasmax", "tasmin","pr"]:
                    vdire = expdire+"/"+var
                    setdirectory(vdire)
                    if not path.exists(vdire+"/script.bash"):
                        script = get_script(conn, sid = sid, member = member, expid = expid, var = var)
                        with open(vdire +"/script.bash", "w") as f:
                            f.write(script)

# Possibility to handle launch of script and concatenation with SUBPROCESS
# But download speed seemed lower, is it due to SUBPROCESS ?         

