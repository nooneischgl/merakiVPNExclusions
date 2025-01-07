# Add VPN Exclusions 


# Installation

## Create venv virtual enviorment 
```python -m venv .venv```

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
git clone
pip install -r requirements.txt
python addVPNExclusions.py -orgID <MerakiOrgID> [-networkName <MerakiNetworkName> | -networkTag <MerakiNetworkTag> | -templateName <MerakiTemplateName>] -exclusionsList <exclusionlistFilename.csv>
```

# Reminders / Gottchas
- **This script does not append put fully replaces any exisiting VPN Exclusions**
- Only IPv4 IPs are allowed
- Major Applications is not currently supported by this script 
