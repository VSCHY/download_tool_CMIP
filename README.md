# download_tool_CMIP
Some tools to help download CMIP6 data

https://esgf-pyclient.readthedocs.io/_/downloads/en/latest/pdf/

## Installation
Create an environment ESGF to run the code : 

        $ conda create -n ESGF -c conda-forge esgf-pyclient pip numpy configparser tqdm

        $ conda activate ESGF

        $ pip install myproxyclient


Then change in /home/usr/anaconda3/envs/ESGF/lib/python3.6/site-packages/pyesgf/search/context.py
At line 200:

        if not ignore_facet_check:
        
            query_dict['facets'] = '*'

Change to :

        if not ignore_facet_check:
         
            query_dict['facets'] = 'null'
            
           
