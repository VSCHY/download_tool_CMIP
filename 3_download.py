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
    if not path.exists(dire+"/script.bash"):
        try:
            os.chdir(dire)
            subprocess.check_call(["bash", "script.bash"])
        except:
            print("NO OROG")
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
                    subprocess.check_call(["bash", "script.bash"])

# Possibility to handle launch of script and concatenation with SUBPROCESS
# But download speed seemed lower, is it due to SUBPROCESS ?         

