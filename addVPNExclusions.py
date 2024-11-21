import meraki
import argparse
import ipaddress
import re
#import batch_helper
import logging
import csv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Handel the Args 
parser = argparse.ArgumentParser(description="Adds VPN Exlusions to Listed Networks / Net Tags")
parser.add_argument("-exclusionsList", action="store", dest="exclusionslist")
parser.add_argument("-orgID", action="store", dest="orgid")
parser.add_argument("-networkName" , action="store", dest="networkname")
parser.add_argument("-networkTag", action="store", dest="networktag")
args = parser.parse_args()

exclusionslist = args.exclusionslist
networktag = args.networktag
networkname = args.networkname
orgid = args.orgid

dashboard = meraki.DashboardAPI(log_path='Logs/')

def getNetworkID(orgID, networkName):
    #Get Network ID based on Network Name
    allNetworks = dashboard.organizations.getOrganizationNetworks(orgID)
    for network in allNetworks:
        if network['name'] == networkName:
            netID = network['id']
            logging.info(f"Network ID {netID} Found for Network Named {networkName}")
    
    return [netID]

def getNetworkIDsfromTag(orgID, networkTag):
    #Get Mulitple Network IDs based on Network Tag
    netIDs = []
    allNetworks = dashboard.organizations.getOrganizationNetworks(orgID)
    for network in allNetworks:
        if networkTag in network['tags']:
            networkName = network['name']
            netIDs.append(network['id'])
            logging.info(f"Network ID {netIDs} Found for Network Named {networkName}")
    
    return netIDs


def readExclusionList(exclusionslist):
    exclusionsPayload = []
    #Open Switch List File
    if exclusionslist:
        with open(exclusionslist, mode='r') as exList:
            reader = csv.reader(exList) 
            rows = list(reader)
            

            #Iterate through each Row starting (not row 2)
            for index, row in enumerate(rows[1:]): 
                print(f"ROW: {row}")
                logging.info(f"Switch List Row: {row}")

                destination = row[0]
                procotol = row[1]
                port = row[2]

                if procotol == "dns":
                    #Check for valid FQDN
                    if is_valid_fqdn(destination):
                        valid_payload={
                            "protocol": procotol,
                            "destination": destination,
                            "port": port
                        }
                        exclusionsPayload.append(valid_payload)
                    else:
                        raise ValueError(f"'{destination}' is not a valid Fully Qualified Domain Name (FQDN).")
                
                if procotol != "dns":
                    #Check for Valid IP or CIDR 
                    if is_valid_ipv4_or_cidr(destination):
                        valid_payload={
                            "protocol": procotol,
                            "destination": destination,
                            "port": port
                        }
                        exclusionsPayload.append(valid_payload)
                    else:
                        raise ValueError(f"'{destination}' is not a valid IP address or CIDR.")
    print("Payload",exclusionsPayload)

    return exclusionsPayload

def addVPNExclusions(exclusionsPayload, networkIDs):
    for network in networkIDs:
        dashboard.appliance.updateNetworkApplianceTrafficShapingVpnExclusions(network, custom = exclusionsPayload)


def is_valid_ipv4_or_cidr(value: str) -> bool:
    """
    Checks if a string is a valid IPv4 address or IPv4 CIDR notation.

    :param value: The string to check.
    :return: True if valid, False otherwise.
    """
    try:
        # Check if it's a valid IPv4 address
        ip = ipaddress.IPv4Address(value)
        return True
    except ipaddress.AddressValueError:
        pass

    try:
        # Check if it's a valid IPv4 CIDR
        network = ipaddress.IPv4Network(value, strict=False)
        return True
    except ipaddress.NetmaskValueError:
        pass
    except ipaddress.AddressValueError:
        pass

    return False

def is_valid_fqdn(fqdn: str) -> bool:
    """
    Checks if a string is a valid Fully Qualified Domain Name (FQDN).
    
    :param fqdn: The string to check.
    :return: True if valid, False otherwise.
    """
    # FQDN regex pattern
    fqdn_regex = re.compile(
        r'^(?=.{1,253}$)'  # Length of FQDN (1-253 characters)
        r'((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+'  # Subdomains and domain labels
        r'[A-Za-z]{2,63}$'  # TLD (2-63 characters)
    )
    return bool(fqdn_regex.match(fqdn))


def main():

    payload = readExclusionList(exclusionslist)

    if networkname: 
        ids = getNetworkID(orgid, networkname)
        addVPNExclusions(payload, ids)
        
    if networktag:
        ids = getNetworkIDsfromTag(orgid, networktag)
        addVPNExclusions(payload, ids)

if __name__ == "__main__":
    main()