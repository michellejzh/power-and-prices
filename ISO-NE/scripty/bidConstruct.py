import csv
import os
import sys
import fileinput


def constructBidStack(myFile):
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
	findPriceChanges(date,hours)

def getKey(item):
	return float(item[0])



def findPriceChanges(date, hours):
	load the file that has the cleared demand on it, by date
	demandFile = "cleared-demand/" + date + "cleareddemand.csv"
	fileReader = open(demandFile, "rU")
	reader  = csv.DictReader(fileReader)
	demands = {}
	for row in reader:
		demands[int(row['Hour Ending'])] = float(row['Day-Ahead Cleared Demand'])

	# for each hour in the cleared demand (should be 24/file):
	# 	for quantity from 0 to maxQuantity of wind added:

	for hour in demands:
		

			go through the (price,quantity) pairs until you hit cleared demand
			eg. sum += pair[1]
			if sum == demand:
				save price pair[0] to new file as for wind = quantity




def saveDayHours(date, hours):
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
		except ValueError:
			print "Error: input must be a string"
			exit()
	else:
		print "Usage: bidConstruct.py <bid file folder>"

	print "Folder: " + str(folder)
	files = os.listdir(folder)
	print "Files: " + str(files)
	numFiles = len(files)
	for i in xrange(1, numFiles):
		path = folder + "/" + files[i]
		constructBidStack(path)




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




