import csv
import sys
import os
import Queue
import numpy as np


def averageWindByDay(windFile):
	with open(windFile, 'rU') as csvfile:
		reader = csv.reader(csvfile, dialect=csv.excel_tab, delimiter=',', quotechar='|')
		row = "placeholder"
		dates = [] # eventually need to write in date order
		days = {} # average saved per date

		reader.next()
		while row[0]!='':
			# mw = np.empty(24, dtype=int) # contains mw for 24 hours
			mw = np.zeros(24, dtype=int)
			hour = 0
			for row in reader:
				print hour, row
				if hour==0:
					dates.append(row[1])
				print row[3]
				print hour
				np.insert(mw,hour,row[3])
				print "now"
				hour += 1
				if hour == 24:
					break
			print mw
			# now average the mw and save in days
			avg = np.average(mw)
			days[row[1]] = avg
			print "Average on " + str(row[1]) + " is " + str(avg)
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