"""
Get the download script from CMIP6 for the simulations.
"""
from CMIP6_dl_tools import tools
from CMIP6_dl_tools import inputs
from CMIP6_dl_tools import connect
from os import path

##################
#
# PARAMETERS
#
openid, password = inputs.load_login()
dfile, experiments, variables, wrkdir = inputs.load_inputs()

test = False

##################
#
# CONNECTION
#
lm, conn = connect.init_connection(openid, password)

##################
#
# CONNECTION
#
a = tools.loadjson(dfile)

# FOR EACH MODEL:
for sid in list(a.keys())[:3]:
    print("**", sid, "**")
    
    dire = wrkdir+"/"+sid
    tools.setdirectory(dire)

    # OROGRAPHY
    if not path.exists(dire+"/script.bash"):
        try:
            script = tools.get_script(conn, sid = sid, var = "orog", realm = "land")
            tools.save_script(script, dire, filename = "script.bash")
        except:
            print("NO OROG")
            tools.save_script("The variable 'orog' is not available", dire, filename = "OROG_ABSENT")
            continue

    # OTHER VARIABLES
    if path.exists(dire+"/script.bash"):
        for member in a[sid][:1]:
            print(" -",member)
            # Ceate directory with member if not exists (function)
            tools.setdirectory(dire+"/"+member)
            for expid in experiments:
                tools.setdirectory(dire + "/" + member + "/" + expid)
                for var in variables:
                    dir_variable = dire + "/" + member + "/" + expid + "/" + var
                    tools.setdirectory(dir_variable)

                    if not path.exists(dir_variable + "/script.bash"):
                        script = tools.get_script(conn, sid = sid, member = member, expid = expid, var = var)
                        tools.save_script(script, dir_variable, filename = "script.bash")
         