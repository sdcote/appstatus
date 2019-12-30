import certifi
import requests

# Updating the CAs the "requests" module uses involves updating the "certifi" trust store
# https://2.python-requests.org//en/latest/user/advanced/#ca-certificates
#
# What this does is try to connect to a site which is protected with our self-signed certificate. If an SSL error is
# experienced, this script will append our root certificate to the end of the existing certificate store.

try:
    print('Checking connection to ServiceNow...')
    test = requests.get('https://servicenow.aepsc.com')
    print('Connection to ServiceNow OK.')
except requests.exceptions.SSLError as err:
    print('SSL Error. Adding custom certs to Certifi store...')
    cafile = certifi.where()
    print(cafile)
    with open('aeproot2014.pem', 'rb') as infile:
        customca = infile.read()
    with open(cafile, 'ab') as outfile:
        outfile.write(customca)
    print('The certificate store has been updated.')
