"""
Create the json files containing all the simulations with
the experiment / variables defined in the search.def file.  
"""
from CMIP6_dl_tools import tools
from CMIP6_dl_tools import inputs
from CMIP6_dl_tools import connect

##################
#
# PARAMETERS 

dfile, experiments, variables,_ = inputs.load_inputs()
openid, password = inputs.load_login()
print(f"List of experiments: {experiments}")
print(f"List of variables: {variables}")

##################
#
# CONNECTION
#
lm, conn = connect.init_connection(openid, password)

##################
#
# Get the different model
#
models = tools.get_sid(conn, exp_id = experiments[0], variable = variables[0])
#
# For each source_id, save in D the members with the required data
#
D = {}
for i, sid in enumerate(models):
    if sid not in D:
       print(sid, i, "/", len(models))
       L = tools.get_member(conn, sid, experiments, variables)
       if len(L)> 0:
           D[sid] = L
           print(" -", len(L), "simulations")

# Save in a json file
tools.savejson(dfile, D)
