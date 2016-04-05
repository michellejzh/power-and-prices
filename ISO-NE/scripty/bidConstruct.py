import csv
import os
import sys
import fileinput


def constructBidStack(myFile, demandFolder):
	if not "2014" in myFile:
		print "Not 2014! Moving on..."
		return

	print "\n~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-"
	print "Constructing bid stack..."
	fileReader = open(myFile, "rU")
	reader  = csv.DictReader(fileReader)

	# make a list for each hour of the day
	# hours = defaultdict(list)
	hours = {}
	for i in xrange(1,25):
		hours[i] = []

	# take from: "Segment 1 Price" to "Segment 10 Price"
	# "Segment 1 MW" to "Segment 10 MW"
	# {price, MW}

	rowNum = 0
	for row in reader:
		rowNum += 1
		for i in xrange(1, 11):
			priceTitle = "Segment " + str(i) + " Price"
			mwTitle = "Segment " + str(i) + " MW"
			try:
				if row[priceTitle] != '' and row[mwTitle] != '':
					# print "Hour: " + str(int(row["Trading Interval"]))
					# print "Dict entry at this hour: " + str(hours[int(row["Trading Interval"])])
					# hourLen = len(hours[int(row["Trading Interval"])])
					hours[int(row["Trading Interval"])].append((row[priceTitle], row[mwTitle]))
			except ValueError:
				break

	# sort the lists by price (first item in tuple)
	for i in xrange(1,25):
		hours[i] = sorted(hours[i], key=getKey, reverse=False)
	myFile = (myFile.split('/'))[1]
	date = myFile[:8]
	# if saveDayHours(date, hours) == 0:
		# findPriceChanges(date,hours, demandFolder)
	if "2014" in date:
		print "SAVING A 2014 THING"
		findPriceChanges(date,hours, demandFolder)

def getKey(item):
	return float(item[0])

def findDemandFile(demandFolder, date):
	myYear = date[0:4]
	# print "Looking for year " + str(myYear)
	yearFolders = os.listdir(demandFolder)
	for y in range(len(yearFolders)):
		if myYear in yearFolders[y]:
			print "Located folder: " + yearFolders[y]
			files = os.listdir(demandFolder + "/" + yearFolders[y])
			for i in xrange(1,len(files)):
				currFile = files[i]
				beginDate = int(currFile[:8])
				endDate = int(currFile[9:17])
				intDate = int(date)
				if intDate >= beginDate:
					if intDate <= endDate:
						# print "Returning " + str(demandFolder + yearFolders[y] + "/" + currFile)
						return demandFolder + "/" + yearFolders[y] + "/" + currFile

	print "*********************************************************"
	print "ERROR: Demand file for date " + str(date) + " not found."
	print "*********************************************************"
	# sys.exit()
	return 0




def findPriceChanges(date, hours, demandFolder):
	print "Finding incremental price changes for date " + str(date) + "..."
	# load the file that has the cleared demand on it, by date
	demandFile = findDemandFile(demandFolder, date)
	if demandFile==0:
		return
	print "Opening file " + str(demandFile)
	fileReader = open(demandFile, "rU")
	reader  = csv.DictReader(fileReader)
	demands = {}

	myDate = date[4:6] + "/" + date[6:] + "/" + date[0:4]
	myDateShort = date[4:6] + "/" + date[6:] + "/" + date[2:4]
	myDateShortest = date[4:6] + "/" + date[6:7] + "/" + date[2:4]
	# Find corresponding demand for each hour
	print "Searching for rows with dates " + myDate
	for row in reader:
		# print "Row's date: " + str(row['Date'])
		rowDate = row['Date']
		try:
			if rowDate == myDate or rowDate == myDate[1:] or rowDate == myDateShort or rowDate == myDateShort[1:] or rowDate == myDateShortest or rowDate == myDateShortest[1:]:
				# print "yes write write write"
				demands[int(row['Hour Ending'])] = float(row['Day-Ahead Cleared Demand'])
		except ValueError:
			print "***********************************************************************"
			print "WARNING: VALUE ERROR FOR VALUE " + str(row['Hour Ending']) + " ON DATE " + str(myDate)
			print "***********************************************************************"			

	yearDateDir = "add-wind-prices/" + date[0:4] + "/"
	if not os.path.exists(yearDateDir):
		os.makedirs(yearDateDir)

	yearDateDir = "add-wind-prices/" + date[0:4] + "/" + date + "/"
	if not os.path.exists(yearDateDir):
		os.makedirs(yearDateDir)
	else:
		print "We already completed this date!"
		return

	print "Writing to directory " + str(yearDateDir)
	for i in xrange(1,25):
		try: 
			hourDemand = demands[i]
			hourSupply = hours[i]
			currYear = date[0:4]

			hourFile = yearDateDir + date + "_" + str(i) + "_adjWindPrices.csv"

			# go through the (price,quantity) pairs until you hit cleared demand
			supplySum = 0.0
			clearingIndex = -1
			# this should go backwards from lowest to highest price
			for p in xrange(len(hourSupply)): 
				supplySum += float(hourSupply[p][1])
				# print "Hour supply pair: " + str(hourSupply[p])
				# print "Supply sum: " + str(supplySum)
				if supplySum >= hourDemand:
					# print "Hour price: " + str(hourSupply[p][0]) 
					clearingIndex = p
					break

			windAdded = 0
			remainder = 0

			# write the header
			with open(hourFile, 'w') as fp:
				writer = csv.writer(fp, delimiter=',')
				writer.writerow(["MW Wind Added", "Price"])	
				# print "Writing to file " + hourFile
				writer.writerow([0,hourSupply[p][0]])

				for p in xrange(clearingIndex, -1, -1):
					pair = hourSupply[p]
					# print "Pair in decrement: " + str(pair)
					remainder = saveMWIncrement(writer, hourFile, windAdded, float(pair[1]), float(pair[0]), remainder)
					windAdded += (float(pair[1]) - remainder)
					if windAdded == hourDemand:
						# print "Demand fully met by wind. Ending write..."
						break
					if pair[0] == 0.0 or pair[0] == '0':
						# print "Price hit 0. Ending write..."
						break
		except KeyError:
			print "***********************************************************************"
			print "WARNING: KEY ERROR FOR HOUR " + str(i) + " ON DATE " + str(myDate)
			print "***********************************************************************"
	print "Completed 24 hours."

# Write the price changes for each bid's MW entirety to the file.
def saveMWIncrement(writer, writePath, windAdded, quantity, price, remainder):
	# print "Writing to path " + writePath
	roundedQuantity = int(quantity+remainder) # rounds down
	remainder = (float(quantity)+float(remainder)) - roundedQuantity
	# with open(writePath, 'a') as fp:
		# writer = csv.writer(fp, delimiter=',')
	for q in xrange(1,roundedQuantity+1):
		row = [windAdded+q, price]
		writer.writerow(row)
	return remainder


def saveDayHours(date, hours):
	print "Saving bids to hours for date " + str(date) + "..."

	yearDateDir = "stacks/" + date[0:4] + "/"
	if not os.path.exists(yearDateDir):
		os.makedirs(yearDateDir)

	yearDateDir = "stacks/" + date[0:4] + "/" + date + "/"
	if not os.path.exists(yearDateDir):
		os.makedirs(yearDateDir)
	else:
		print "We already completed this date!"
		return 1

	print "Writing to directory " + yearDateDir
	for hour in hours:
		writePath = yearDateDir  + str(date) + "_hour" + str(hour) + "_" + "bidStack.csv"
		# print "Writing to path " + writePath 
		with open(writePath, 'w') as fp:
			writer = csv.writer(fp, delimiter=',')
			writer.writerow(["Price", "Quantity"])
			bids = hours[hour]
			for bid in bids:
				row = [float(bid[0]),float(bid[1])]
				writer.writerow(row)
	return 0


if __name__ == '__main__':
	if len(sys.argv) > 1:
		try:
			folder = str(sys.argv[1])
			demandFolder = str(sys.argv[2])
		except ValueError:
			print "Error: input must be a string"
			exit()
	else:
		print "Usage: bidConstruct.py <bid file folder> <demand file folder>"

	print "Folder: " + str(folder)
	files = os.listdir(folder)
	numFiles = len(files)
	print "Number of files: " + str(numFiles)
	for i in xrange(1,numFiles):
		path = folder + "/" + files[i]
		constructBidStack(path, demandFolder)




