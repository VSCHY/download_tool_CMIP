"""
Load the .def files with ConfigParser
"""

import configparser


def load_inputs():
    """
    Load the parameters for the download in the search.def file.
    
    Parameters:
    -----------
    None
    
    Returns:
    --------
    dfile (str): directory of the json file with the model/member
        with the corresponding experiments/variables available.
    experiments (list): list of experiment to download.
    variables (list): list of variables to download.
    wrkdir (str): directory where the files will be downloaded.
    
    ----------------------------------------------------
    """
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
    """
    Load the user id and password from the config.def file.
    
    Parameters:
    -----------
    None
    
    Returns:
    --------
    openid (str): user id.
    password (str)
    
    ----------------------------------------------------
    """
    config=configparser.ConfigParser()
    config.read("config.def")
    openid=config.get("OverAll", "openid")
    password=config.get("OverAll", "password")
    return openid, password
