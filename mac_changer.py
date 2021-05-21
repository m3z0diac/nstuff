#!/usr/bin/env python

import subprocess
import optparse
import re

def getArg():
	parser = optparse.OptionParser()
	parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
	parser.add_option("-m", "--mac", dest="new_mac", help="New Mac address")
	(options, arguments) = parser.parse_args() 
	if not options.interface:
		parser.error("[-] spicefy an interface")
	elif not options.new_mac:
		parser.error("[-] spicefy an new mac")
	return options


def mac_changer(interface, new_mac):

	print("[+] changing MAC address for " + interface + " to " + new_mac)
	subprocess.call(["ifconfig", interface, "down"])         #more secure
	subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
	subprocess.call(["ifconfig", interface, "up"])



options= getArg()

mac_changer(options.interface, options.new_mac)

ifconfig_result = subprocess.call(["ifconfig", options.interface])







