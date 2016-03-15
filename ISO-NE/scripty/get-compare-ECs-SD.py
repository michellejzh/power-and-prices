import urllib2
import base64
import ssl
import csv
import json
from pprint import pprint
import untangle

def getECs(date,username,password):
	# get the energy costs from the LMP files
	base = "https://webservices.iso-ne.com/api/v1.1"
	path = "/hbdayaheadenergyoffer/day/"
	url = base + path + date + ".xml"

	# Call our GET request
	request = urllib2.Request(url)
	print "Request to", url
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)
	# bad practice but good enough for now
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	try:
		result = urllib2.urlopen(request, context=ctx)
	except urllib2.HTTPError:
		print "Day " + str(date) + " does not exist. Continuing to next day.."
		return

	result = result.read()
	xml_result = untangle.parse(result)
	print xml_result

	# lines = xml_result.SOMESTUFFWECHANGEHERE
	writePath = "ECs/" + date + "EnergyComponents.csv"
	with open(writePath, 'w') as fp:
		writer = csv.writer(fp, delimiter=',')
		# then do stuff to the file we're writing to
		pass


def compareWithSDCalculations():
	# how different is this from what we calculated to balance supply and demand?
	pass

if __name__ == '__main__':
	getECs("121212","michelle_zheng@brown.edu","w00lden1")