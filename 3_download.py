"""
Download the files.
"""
from CMIP6_dl_tools import tools
from CMIP6_dl_tools import inputs
from CMIP6_dl_tools import connect
import os
from os import path
import subprocess


##################
#
# PARAMETERS
#
openid, password = inputs.load_login()
dfile, experiments, variables, wrkdir = inputs.load_inputs()
 
##################
#
# CONNECTION
#
lm, conn = connect.init_connection(openid, password)

##################
#
# DOWNLOAD
#

a = tools.loadjson(dfile)

for sid in list(a.keys())[:3]:
    print("**", sid, "**")
    dire = wrkdir+"/"+sid

    # OROGRAPHY
    os.chdir(dire)
    if path.exists(dire+"/script.bash"): 
        subprocess.call(["bash", "script.bash"])
    else:
        print(" - NO OROG")
        with open(wrkdir + "/out.log", "a") as f:
            f.write("source_id: {0} has no orog variable\n".format(sid))
        continue

    # OTHER VARIABLES
    if path.exists(dire+"/script.bash"):
        for member in a[sid][:1]:
            print(" -", member)
            for expid in experiments:
                for var in variables:

                    os.chdir(dire + "/" + member + "/" + expid + "/" + var)
                    print(f" - {sid}, {member}, {expid}, {var}")

                    lm, conn = connect.init_connection(openid, password)

                    try:
                       subprocess.check_call(["bash", "script.bash"])
                    except:
                       with open(wrkdir + "/out.log", "a") as f:
                           f.write("Issue with downloading file:\n")
                           f.write("source_id: {0}, member: {1},experimental_id: {2}, variable: {3}\n".format(sid, member, expid, var))