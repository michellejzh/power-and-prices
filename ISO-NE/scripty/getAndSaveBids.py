import urllib2
import base64
import ssl
import csv
import json
from pprint import pprint
import untangle

# ===================================================================
# http://docs.python-guide.org/en/latest/scenarios/xml/
# https://github.com/stchris/untangle/blob/master/examples.py
# https://webservices.iso-ne.com/docs/v1.1/data_ns0.html#type_HbEnergyOffer
# https://webservices.iso-ne.com/docs/v1.1/data_ns0.html#type_Segment

# LAST DATE LOOKED AT: 20131231

def getDates(username,password):
	for year in range(2014,2015):
		for month in range(1,13):
			if month < 10:
				month = "0" + str(month)
			for day in range(1,32):
				if day < 10:
					day = "0" + str(day)
				date = str(year) + str(month) + str(day)
				print "DATE: " + str(date)
				getAndSaveDay(date,username,password)



def getDemands(username,password):
	date = "20111010"
	getDAMDemand(date,username,password)

	# for year in range(2013,2014):
	# 	for month in range(6,13):
	# 		if month < 10:
	# 			month = "0" + str(month)
	# 		for day in range(1,32):
	# 			if day < 10:
	# 				day = "0" + str(day)
	# 			date = str(year) + str(month) + str(day)
	# 			print "DATE: " + str(date)
	# 			getDAMDemand(date,username,password)


# want: http://www.iso-ne.com/isoexpress/web/reports/load-and-demand/-/reports/dmnd-da-hourly-cleared?p_auth=9rv1KdWO
def getDAMDemand(date,username,password):
	base = "https://webservices.iso-ne.com/api/v1.1"
	path = "/dayaheadhourlydemand/day/"
	# path = "/dayaheadhourlydemand"
	path2 = "/location/SYSTEM"
	# /dayaheadhourlydemand/day/{day}/location/{locationId}
	url = base + path + date + path2 + ".xml"

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
	print result
	xml_result = untangle.parse(result)

	lines = xml_result.children
	for line in lines:
		print str(line.children) + "\n"



def getAndSaveDay(date,username,password):
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
	lines = xml_result.HbDayAheadEnergyOffers.HbDayAheadEnergyOffer
	writePath = "bids/" + date + "HbDayAheadEnergyOffers.csv"
	with open(writePath, 'w') as fp:
		writer = csv.writer(fp, delimiter=',')

		# write the header, obnoxiously
		row = []
		row.append('Day')
		row.append('Trading Interval')
		row.append('Masked Lead Participant ID')
		row.append('Masked Asset ID')
		row.append('Must Take Energy')
		row.append('Maximum Daily Energy Available')
		row.append('Economic Maximum')
		row.append('Economic Minimum')
		row.append('Cold Startup Price')
		row.append('Intermediate Startup Price')
		row.append('Hot Startup Price')
		row.append('No Load Price')
		row.append('Segment 1 Price')
		row.append('Segment 1 MW')
		row.append('Segment 2 Price')
		row.append('Segment 2 MW')
		row.append('Segment 3 Price')
		row.append('Segment 3 MW')
		row.append('Segment 4 Price')
		row.append('Segment 4 MW')
		row.append('Segment 5 Price')
		row.append('Segment 5 MW')
		row.append('Segment 6 Price')
		row.append('Segment 6 MW')
		row.append('Segment 7 Price')
		row.append('Segment 7 MW')
		row.append('Segment 8 Price')
		row.append('Segment 8 MW')
		row.append('Segment 9 Price')
		row.append('Segment 9 MW')
		row.append('Segment 10 Price')
		row.append('Segment 10 MW')
		row.append('Claim 10')
		row.append('Claim 30')
		row.append('Unit Status')
		writer.writerow(row)

		count = 0
		for line in lines:
			fields = [] 

			count += 1
			row = []
			hasMaxDaily = 0
			for child in line.children:
				# print child
				field = (str(child).split(' '))[1].replace('<','').replace('>','')
				fields.append(field)
				if field == "MaxDailyEnergy":
					hasMaxDaily = 1
				if field == "EconomicMax" and hasMaxDaily == 0:
					row.append('')
				# print "Field, Entry: " + str(field), str(child.cdata)
				if field == "BeginDate":
					date = child.cdata.split('T')
					# print "After splitting:", str(date)
					row.append(date[0])
					row.append(int(date[1][:2])+1)
				elif field == "Segments":
					segments = 0					
					for seg in child.children:
						for e in seg.children:
							row.append(e.cdata)
							segments += 1
					while segments < 20:
						segments += 1
						row.append('')
				else:
					row.append(child.cdata)
			writer.writerow(row)


if __name__ == '__main__':
	username = "michelle_zheng@brown.edu"
	password = "w00lden1"
	getDates(username,password)
	# getDemands(username,password)

