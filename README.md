# Add VPN Exclusions 


# Installation

## Clone Repo and Go to Project Folder
``` git clone https://github.com/nooneischgl/merakiVPNExclusions.git```

``` cd merakiVPNExclusions```

## Create venv virtual enviorment 
```python -m venv .venv```

## Install Python Dependencies 
```pip install -r requirements.txt```

## Activate venv
#### PowerShell / Windows 
``` .venv/Scripts/Activate.ps1 ```
#### macOS / Linux
``` source .venv/bin/activate ```

## Set API Key
#### PowerShell / Windows 
``` $Env:MERAKI_DASHBOARD_API_KEY = "APIKeyHere"```
#### macOS / Linux
```export MERAKI_DASHBOARD_API_KEY=APIKeyHere```


# Usage 
**Arguments are case sensitive**  
```
python addVPNExclusions.py -orgID <MerakiOrgID> [-networkName <MerakiNetworkName> | -networkTag <MerakiNetworkTag> | -templateName <MerakiTemplateName>] -exclusionsList <exclusionlistFilename.csv>
```
- Provide your Meraki Org ID with ```-orgID```
- Select which network, network Tag or template you want to be configured with the following Args
  - ```-networkName```
  - ```-networkTag```
  - ```-templateName```
- Provide what VPN exclusions you want configured using the a CSV file see the provided example file **exclusionListExample.csv** `-exclusionsList`

# Reminders / Gottchas
- **This script does not append put fully replaces any exisiting VPN Exclusions**
- Only IPv4 IPs are allowed
- Major Applications is not currently supported by this script 
