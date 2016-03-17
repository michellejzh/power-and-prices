import urllib2
import base64
import ssl
import csv
import json
from pprint import pprint
import untangle

# for the DA LMP files
def getECFromLMP(myFile):
	print "Opening", myFile
	with open(myFile, 'rU') as csvfile:
		r = csv.reader(csvfile, dialect=csv.excel_tab, delimiter=',', quotechar='|')
		fileSeg = myFile.split('/')
		underscored = fileSeg[2].split('_')
		print underscored
		dateLow = underscored[2]
		dateHigh = underscored[3] 

		writePath = fileSeg[0] + "/" + fileSeg[1] + "/1_trimmed/" + dateLow + "-" + dateHigh[0:8] + "_TRIM_clearedDemand.csv"
		with open(writePath, 'w') as fp:
			w = csv.writer(fp, delimiter=',')
			count = 0
			for row in r:
				count += 1
				if count > 4 and count != 6:
					if row[0] == '"T"':
						break
					currRow = [row[1].replace('"',''), row[2].replace('"',''), row[3].replace('"','')]
					w.writerow(currRow) #write the 5th line
			print "Rewrote file " + str(myFile)


# get the price resulting from balancing supply and demand
def getPriceFromSD():
	# how different is this from what we calculated to balance supply and demand?
	pass

if __name__ == '__main__':
	if len(sys.argv) > 1:
		try:
			ECfolder = str(sys.argv[1])
			SDFolder = str(sys.argv[2])
		except ValueError:
			print "Error: input must be a string"
			exit()
	else:
		print "Usage: get-compare-ECs-SD.py <lmps_2010-2014> <add-wind-prices>"

	print "EC folder: " + str(folder)
	print "SD folder: " + str(folder)
	
	files = os.listdir(folder)
	numFiles = len(files)
	print "Number of files: " + str(numFiles)
	for i in xrange(1,numFiles):
		path = folder + "/" + files[i]
		getECFromLMP()


# def getECs(date,username,password):
# 	# get the energy costs from the LMP files
# 	base = "https://webservices.iso-ne.com/api/v1.1"
# 	path = "/hbdayaheadenergyoffer/day/"
# 	url = base + path + date + ".xml"

# 	# Call our GET request
# 	request = urllib2.Request(url)
# 	print "Request to", url
# 	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
# 	request.add_header("Authorization", "Basic %s" % base64string)
# 	# bad practice but good enough for now
# 	ctx = ssl.create_default_context()
# 	ctx.check_hostname = False
# 	ctx.verify_mode = ssl.CERT_NONE

# 	try:
# 		result = urllib2.urlopen(request, context=ctx)
# 	except urllib2.HTTPError:
# 		print "Day " + str(date) + " does not exist. Continuing to next day.."
# 		return

# 	result = result.read()
# 	xml_result = untangle.parse(result)
# 	print xml_result

# 	# lines = xml_result.SOMESTUFFWECHANGEHERE
# 	writePath = "ECs/" + date + "EnergyComponents.csv"
# 	with open(writePath, 'w') as fp:
# 		writer = csv.writer(fp, delimiter=',')
# 		# then do stuff to the file we're writing to
# 		pass