import configparser
# json output file
def load_inputs(output_dir = True):

    search=configparser.ConfigParser()
    search.read("search.def")
    dfile=search.get("OverAll", "dfile", fallback="./Models_CMIP6.json")

    # experiments
    experiments=search.get("OverAll", "experiments", fallback = "historical")
    experiments = experiments.split(" ")

    # variables
    variables = search.get("OverAll", "variables", fallback = "pr")
    variables = variables.split(" ") 

    wrkdir = search.get("OverAll", "wrkdir", fallback = None)

    return dfile, experiments, variables, wrkdir

def load_login():
    config=configparser.ConfigParser()
    config.read("config.def")
    openid=config.get("OverAll", "openid")
    password=config.get("OverAll", "password")
    return openid, password