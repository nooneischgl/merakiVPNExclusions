# Add VPN Exclusions 


# Installation

```
git clone
pip install -r requirements
python addVPNExclusions.py -orgID <MerakiOrgID> [-networkName <MerakiNetworkName> | -networkTag <MerakiNetworkTag>] -exclusionlist <exclusionlistFilename.csv>
```

# Usage 
**Add the following Environment Variables for Authentication**
- API Key - `export MERAKI_DASHBOARD_API_KEY=<YOUR_KEY_HERE>`


# Reminders / Gottchas
- ** This script does not append put fully replaces any exisiting VPN Exclusions **
- Only IPv4 IPs are allowed
- Major Applications is not currently supported by this script 