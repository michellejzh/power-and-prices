import csv
import os
import sys
import operator
from shutil import copyfile


# next step: get copies of the hour files for each percentile chunk all together in one folder
# or even one file

def orderByDemand():
	demandDict = saveDemandsToDict()
	print "Sorting..."
	sortedDemands = sorted(demandDict.items(), key=operator.itemgetter(1))
	print "Writing..."

	hourFile = "sorted_demands/sortedHourlyDemand.csv"
	with open(hourFile, 'w') as fp:
		writer = csv.writer(fp, delimiter=',')
		writer.writerow(["Timestamp","Date","Hour","Demand"])
		for hour in sortedDemands:
			currDate = hour[0][:9]
			currHour =  hour[0][9:]
			writer.writerow([hour[0],currDate,currHour,hour[1]])

	numHours = len(sortedDemands)
	print "Number of hours: " + str(numHours)
	tenth = int(numHours/10)
	half = int(numHours/2)
	savePercentiles(sortedDemands[0:tenth], "sorted_demands/bottom10PercDemandHours.csv")
	savePercentiles(sortedDemands[half-(tenth/2):half+(tenth/2)], "sorted_demands/median10PercDemandHours.csv")
	savePercentiles(sortedDemands[numHours-tenth-1:numHours-1], "sorted_demands/top10PercDemandHours.csv")


def savePercentiles(sortedDemands, filename):
	with open(filename, 'w') as fp:
		writer = csv.writer(fp, delimiter=',')
		writer.writerow(["Timestamp","Demand"])
		for hour in sortedDemands:
			writer.writerow([hour[0],hour[1]])
	print "Finished " + str(filename)


def saveDemandsToDict(): # for all hours of all years
	demandFolder = "cleared_demand_2010-2014"
	demands = {} # demands[YYYMMDDHR] = demand value
	yearFolders = os.listdir(demandFolder)
	for y in range(1,len(yearFolders)-1):
		files = os.listdir(demandFolder + "/" + yearFolders[y])
		for i in xrange(1,len(files)):
			demandFile = demandFolder + "/" + yearFolders[y] + "/" + files[i]
			print "Opening file " + str(demandFile)
			fileReader = open(demandFile, "rU")
			reader  = csv.DictReader(fileReader)

			for row in reader:
				try:
					date = row['Date'].split('/')
					month = int(date[0])
					if month < 10:
						month = "0" + str(month)
					day = int(date[1])
					if day < 10:
						day = "0" + str(day)
					year = int(date[2])
					if year < 2000:
						year = "20" + str(year)
					hour = row['Hour Ending']
					if hour < 10:
						hour = "0" + str(hour)
					date = str(year)+str(month)+str(day)+str(hour)
					demands[date] = float(row['Day-Ahead Cleared Demand'])
					
				except ValueError:
					print "Boo value error. This row sucks: " + str(row) 
	return demands


def organizePercentileFolders(filename):
	folderTitle = filename.split(".")[0] + "/"
	if not os.path.exists(folderTitle):
		os.makedirs(folderTitle)

	fileReader = open(filename, "rU")
	reader  = csv.DictReader(fileReader)
	for row in reader:
		try:
			fileDate = row["Timestamp"]
			fileHour = int(fileDate[8:])
			fileDate = fileDate[:8]

			# do the search through the folders
			demandFile = "add-wind-prices/" + str(fileDate[:4]) + "/" + str(fileDate) + "/" + str(fileDate) + "_" + str(fileHour) + "_adjWindPrices.csv"
			try:
				copyfile(demandFile, folderTitle + str(fileDate) + "_" + str(fileHour) + "_adjWindPrices.csv")
			except IOError:
				print "Couldn't find the file " + folderTitle + str(fileDate) + "_" + str(fileHour) + "_adjWindPrices.csv"
		except ValueError:
			print "value error sux for row " + str(row)
	print "Completed file copying for " + str(filename)



if __name__ == '__main__':
	# orderByDemand()
	organizePercentileFolders("sorted_demands/bottom10PercDemandHours.csv")
	organizePercentileFolders("sorted_demands/median10PercDemandHours.csv")
	organizePercentileFolders("sorted_demands/top10PercDemandHours.csv")



