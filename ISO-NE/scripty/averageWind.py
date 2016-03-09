import csv
import sys
import os
import Queue
import numpy as np
import math


def averageWindByDay(windFile):
	with open(windFile, 'rU') as csvfile:
		reader = csv.reader(csvfile, dialect=csv.excel_tab, delimiter=',', quotechar='|')
		row = "placeholder"
		dates = [] # eventually need to write in date order
		days = {} # average saved per date

		reader.next()
		prevDay = "1/1/11"
		mw = []
		# fill with all the hours in the day
		for row in reader:
			currDay = row[1]
			if currDay != prevDay:
				if mw == []:
					print "BREAKING!"
					break
				# add the previous day to the list of dates
				dates.append(prevDay)
				# now average the mw of prevDay and save in days
				avg = np.average((np.array(mw)).astype(float))
				days[prevDay] = avg
				print "Average on " + str(row[1]) + " is " + str(avg)
				mw = []
			mw.append(row[3])
			prevDay = currDay

	print "-----------------------------------------"
	print dates
	# print days
	savePairs("avgd-"+windFile, dates, days)



def savePairs(writePath, dates, days):
	with open(writePath, 'a') as fp:
		writer = csv.writer(fp, delimiter=',')
		for day in dates:
			line = [day, days[day]]
			writer.writerow(line)
			print "Saving " + str(line)


if __name__ == '__main__':
	if len(sys.argv) > 1:
		try:
			windFile = str(sys.argv[1])
			averageWindByDay(windFile)
		except ValueError:
			print("Error: input must be a string")
			exit()
	else:
		print("Usage: averageWind.py <wind-file>")