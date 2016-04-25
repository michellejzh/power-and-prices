import csv
import sys
import os
import Queue


def matchByDate(spotFile):
	with open(spotFile, 'rU') as csvfile:
		priceReader = csv.reader(csvfile, dialect=csv.excel_tab, delimiter=',', quotechar='|')
		# put spot date-price pairs into dict
		pairs = {}
		for row in priceReader:
			# print row
			spotDate = row[0]
			spotPrice = row[1]
			pairs[spotDate] = spotPrice
		# print pairs

		# then assign them to full dates by match. leave blank if missing
		finalPairs = {}
		dates = Queue.Queue(0)
		writePath = "fixed-" + spotFile
		csvfile.seek(0)
		for row in priceReader:
			date = row[2]
			dates.put(date)
			if date in pairs:
				finalPairs[date] = pairs[date]
			else:
				finalPairs[date] = ""
		savePairs(writePath, finalPairs, dates)


"""
Save correct date-price pairs in date order.
"""
def savePairs(writePath, pairs, dates):
	with open(writePath, 'a') as fp:
		writer = csv.writer(fp, delimiter=',')
		print pairs
		prevVal = ""
		key = "placeholder"
		while not dates.empty() and key != "":
			key = dates.get()
			val = pairs[key]
			# carrying prices over weekends and holidays
			if val == "":
				val = prevVal
			line = [key, val]
			writer.writerow(line)
			print "Saving " + str(line)
			prevVal = val
	



if __name__ == '__main__':
	# python adjustSpot.py hh-spot.csv
	if len(sys.argv) > 1:
		try:
			spotFile = str(sys.argv[1])
			matchByDate(spotFile)
		except ValueError:
			print("Error: input must be a string")
			exit()
	else:
		print("Usage: adjustSpot.py <date-matching-file>")








