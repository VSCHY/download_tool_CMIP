# download_tool_CMIP
Some tools to help download CMIP6 data

https://esgf-pyclient.readthedocs.io/_/downloads/en/latest/pdf/

## Installation
Create an environment ESGF to run the code : 
```
conda create -n ESGF -c conda-forge esgf-pyclient pip numpy configparser

conda activate ESGF

pip install myproxyclient
```

## INPUT FILE
To make a request you have to complete both .def files:
- config.def with your IDs
- search.def with the parameter of your request

### config.def
**openid =** *your_id*
**password =** *your_password*

*(Create an account on https://esgf-node.llnl.gov/login/)*

### search.def
- Name of the json file that will contain all the model/member compatible with your request
 
**dfile =** *my_request.json*

- list of the experiment you consider

**experiments =** *historical ssp585*

- list of the variables you want to download

**variables =** *pr tasmax*

- directory where you want to save the downloads

**wrkdir =** */dir/to/save/files/CMIP6*


## DOWNLOAD
Launch the search and save all the models/member with the experiments / variables you are interested in:

1. `python 1_get_memberlist.py`

Create the directory structure for the download and prepare the Script.bash file to download the files:

2. `python 2_get_downloadfile.py`

Launch the download:

3. `python 3_download.py`

*During this third step, the download may be blocked due to the waiting of the server.*

*It may also stops after 8 hours (credentials available 8 hours).*

*You have to launch it again, it will pass the already downloaded files.*
