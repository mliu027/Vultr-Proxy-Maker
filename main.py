import json
import sys
import os
from vultr import Vultr

try:
	with open("api_key.txt","r") as f:
		api_key = f.read()
		f.close()
except IOError:
	print "api_key.txt not found"
	api_key = raw_input("Enter Api Key: ")
	with open("api_key.txt", "w") as f:
		f.write(api_key)
		f.close()
	
def wait():
	raw_input("Press Enter to Continue")
	os.system('clear')
	
def DestroyAllServers():
	servers = vultr.server_list()
	for server in servers:
		vultr.server_destroy(server)
	os.system('clear')
	print "All Servers Destroyed\n"
	raw_input("Press Enter to Continue")
	os.system('clear')
	
def ListServerIps():
	filename = raw_input("Enter File Name: ")
	with open(filename, "w") as f:	
		servers = vultr.server_list()
		for server in servers:
			f.write(servers[server]["main_ip"] +":3128\r\n")
		f.close()
	print 'IPs Written to ' + filename
	wait()
	
def ChangeApiKey():
	NewApiKey = raw_input("Enter New Api Key: ")
	UpdateApiKey(NewApiKey)
	print "Api Key Updated"
	wait()

def UpdateApiKey(NewKey):
	global vultr
	vultr = Vultr(NewKey)
	with open("api_key.txt", "w") as f:
		f.write(NewKey)
		f.close()
		
#Will Create Ubuntu 14.04 x64 Servers in LA
def CreateServers():
	regions = vultr.regions_list()
	for region in regions:
		if regions[region]["name"] == 'Los Angeles':
			DCID = regions[region]["DCID"]
			break
	NumberOfServers = raw_input("Enter the Number of Servers: ")
	while True:
		try:
			NumberOfServers = int(NumberOfServers)
			break
		except ValueError:
			NumberOfServers = raw_input("Please Enter a Number: ")
	
	scripts = vultr.startupscript_list()
	ScriptName = raw_input("Enter Startup Script Name (if not found no startup script will be used): \n")
	found = False
	for script in scripts:
		if scripts[script]['name'] == ScriptName:
			SCRIPTID = scripts[script]['SCRIPTID']
			print "Script Found"
			found = True
			break
	if not found:
		print ScriptName +" Script not found. No script will be used."
	servers = vultr.plans_list()
	price = raw_input("Enter Price(XX.XX): ")
	os.system('clear')
	for server in servers:
		if servers[server]['price_per_month'] == price:
			print "ID: " + str(servers[server]['VPSPLANID']) + " " + str(servers[server]['name'])
	VPSPLANID = raw_input("Enter Plan ID: ")
	oslist = vultr.os_list()
	for OS in oslist:
		if "Ubuntu 14.04 x64" in oslist[OS]['name']:
			print "Ubuntu 14.04 x64 Found"
			OSID = oslist[OS]['OSID']
	for i in range(0,NumberOfServers):
		vultr.server_create(DCID, VPSPLANID, OSID,scriptid = SCRIPTID)
	
	wait()
	
def main():
	global api_key
	global vultr
	vultr = Vultr(api_key)
	os.system('clear')
	while True:
		i=int(raw_input('Main Menu\n1) Write IPs to txt\n2) Destroy All Servers\n3) Change API Key\n4) Current API Key\n5) Create Servers\n6) Exit\n'))
		os.system('clear')
		if i == 1:
			ListServerIps()
		elif i == 2:
			i = raw_input('Are you sure you want to destroy all servers?(Y/n)')
			if i == 'Y':
				DestroyAllServers()
			elif i == 'n':
				pass
			else:
				print "Y/n only"
		elif i == 3:
			ChangeApiKey()			
		elif i == 4:
			print vultr.api_key
		elif i == 5:
			CreateServers()
		elif i == 6:
			sys.exit(0)

			
if __name__ == "__main__":
	main()