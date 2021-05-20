#!/usr/bin/env python

import scapy.all as scapy
import optparse


def getArg():
	parser = optparse.OptionParser()
	parser.add_option("-t", "--target", dest="target", help="target IP/ IP range")
	(options, arg) = parser.parse_args()
	return options



def scan(ip):

	arp_requests = scapy.ARP(pdst=ip)   #send requests how has ip
	#arp_requests.show()
	brodcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")  #send packet from my mac address to ff:ff:ff:ff:ff:ff 
	#brodcast.show() 
	arp_requests_brocast = brodcast/arp_requests
	#ip_requests_brocast.show()
	answerd_list = scapy.srp(arp_requests_brocast, timeout=2)[0]
	unanswerd_list = scapy.srp(arp_requests_brocast, timeout=2)[1]
	#print(unanswerd_list.summary())
	
	clients_list = []
	for el in answerd_list:
		#print(el[0].show())
		#print(el[1].psrc+"\t|\t"+el[1].hwsrc)
		clients_list.append({"ip":el[1].psrc,"mac":el[1].hwsrc})
	return clients_list

def print_result(client_result):
	print("-----------------------------------------\nip address"+"\t|\t"+"Mac address\n-----------------------------------------")

	for client in client_result:
		print(client["ip"] + "\t\t" + client["mac"])
	
options = getArg()
scan_result = scan(options.target)
print_result(scan_result)