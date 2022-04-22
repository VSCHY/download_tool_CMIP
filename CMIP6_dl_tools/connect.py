from pyesgf.search import SearchConnection
from pyesgf.logon import LogonManager
import os


def init_connection(openid,password):
    lm = LogonManager()
    lm.logoff()
    lm.logon_with_openid(openid, password = password, bootstrap = True)
    t = "http://esgf-node.llnl.gov/esg-search"
    print("Connect")
    conn = SearchConnection(t, distrib=True)

    os.environ["ESGF_PYCLIENT_NO_FACETS_STAR_WARNING"] = "1"
    return lm, conn