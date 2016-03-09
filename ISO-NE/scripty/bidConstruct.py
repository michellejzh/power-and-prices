import csv
import os
import sys
import fileinput


def constructBidStack(myFile, demandPath):
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
		hours[i] = sorted(hours[i], key=getKey)
	myFile = (myFile.split('/'))[1]
	date = myFile[:8]
	saveDayHours(date, hours)
	findPriceChanges(date,hours, demandPath)

def getKey(item):
	return float(item[0])



def findPriceChanges(date, hours, demandPath):
	print "Finding incremental price changes for date " + str(date) + "..."
	# load the file that has the cleared demand on it, by date
	demandFile = demandPath + "/" + date + "cleareddemand.csv"
	print "Opening file " + str(demandFile)
	fileReader = open(demandFile, "rU")
	reader  = csv.DictReader(fileReader)
	demands = {}

	# Find corresponding demand for each hour
	for row in reader:
		demands[int(row['Hour Ending'])] = float(row['Day-Ahead Cleared Demand'])

	# wind added == demand reduced, since you effectively shift to the left
	# but for our graphical purposes, insert on the far left as well?
		# --> no, runtime gets bad

	for i in xrange(1,25):
		hourDemand = demands[i]
		hourSupply = hours[i]
		hourFile = "add-wind-prices/" + date + "_" + str(i) + "_adjWindPrices.csv"
		# go through the (price,quantity) pairs until you hit cleared demand
		windAdded = 0
		for pair in hour:
			saveMWIncrement(hourFile, windAdded, int(pair[1]), float(pair[0]))
			windAdded += int(pair[1])
			if windAdded == demand:
				break

# Write the price changes for each bid's MW entirety to the file.
def saveMWIncrement(writePath, windAdded, quantity, price):
	print "Writing to path " + writePath 
	with open(writePath, 'w') as fp:
		writer = csv.writer(fp, delimiter=',')
		writer.writerow(["MW Wind Added", "Price"])	
	for q in xrange(1,quantity+1):
		row = [windAdded+q, price]
		writer.writerow(row)


def saveDayHours(date, hours):
	print "Saving bids to hours for date " + str(date) + "..."
	for hour in hours:
		directory = str(date) + "_stacks/"
		if not os.path.exists(directory):
		    os.makedirs(directory)
		writePath = directory  + str(date) + "_hour" + str(hour) + "_" + "bidStack.csv"
		print "Writing to path " + writePath 
		with open(writePath, 'w') as fp:
			writer = csv.writer(fp, delimiter=',')
			writer.writerow(["Price", "Quantity"])
			bids = hours[hour]
			for bid in bids:
				row = [float(bid[0]),float(bid[1])]
				writer.writerow(row)


if __name__ == '__main__':
	if len(sys.argv) > 1:
		try:
			folder = str(sys.argv[1])
			demandPath = str(sys.argv[2])
		except ValueError:
			print "Error: input must be a string"
			exit()
	else:
		print "Usage: bidConstruct.py <bid file folder> <demand file folder>"

	print "Folder: " + str(folder)
	files = os.listdir(folder)
	print "Files: " + str(files)
	numFiles = len(files)
	for i in xrange(1, numFiles+1):
		path = folder + "/" + files[i]
		constructBidStack(path, demandPath)




# UNNECESSARY FOR THE NEW FORMAT =====================================================
# def cutHeader(myFile):
# 	# r = fileinput.input(myFile, inplace=True) # sys.stdout is redirected to the file
# 	# print r
# 	# for i in xrange(4):
# 	# 	r.next() #skip 4 lines
# 	# print r.next() #print the 5th line
# 	# r.next() #skip the 6th line

# 	print "Opening", myFile
# 	with open(myFile, 'rU') as csvfile:
# 		r = csv.reader(csvfile, dialect=csv.excel_tab, delimiter=',', quotechar='|')
# 		w = csv.writer(sys.stdout)
# 		count = 0
# 		for row in r:
# 			# print count
# 			# print row
# 			count += 1
# 			if count >= 4 and count != 6:
# 				w.writerow(row) #write the 5th line
# 				print row
# 		print "Rewrote file " + str(myFile)




