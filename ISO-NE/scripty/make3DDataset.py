import csv
import os

def make3DDataset(year):
	# writePath = "time-mw-price_2010-2014.csv"
	writePath = "time-mw-price_SHORTEST.csv"
	with open(writePath, 'w') as fp:
		writer = csv.writer(fp, delimiter=',')
		writer.writerow(["Timestamp","MW Added","Price","Demand","Gas Percentage"])
		years = os.listdir("add-wind-prices")
		# for y in xrange(1,len(years)):
		# for y in xrange(1,2):
		gasDict, demDict = loadOtherVars()
		y = year
		days = os.listdir("add-wind-prices/" + years[y])
		for d in xrange(1,len(days)):
		# for d in xrange(1,2):
			hours = os.listdir("add-wind-prices/" + years[y] + "/" + days[d])
			for h in xrange(1,25):
				myFile = days[d] + "_" + str(h) + "_adjWindPrices.csv"
				# print "Opening file " + myFile
				try:
					fileReader = open("add-wind-prices/" + years[y] + "/" + days[d] + "/" + myFile, "rU")
					reader  = csv.DictReader(fileReader)
					done = 0
					for row in reader:
						if done == 0: # skip the first row
							done = 1
						else:
							if float(row['MW Wind Added']) > 12000.0:
								print "More than 12 KW added. Breaking..."
								break
							pieces = myFile.split("_")
							myHour = int(pieces[1])
							if myHour < 10:
								myHour = "0" + str(myHour)
							timestamp = pieces[0] + str(myHour)
							writer.writerow([timestamp,row['MW Wind Added'],row['Price'],demDict[timestamp],gasDict[pieces[0]]])
				except IOError:
					print "Failed to open file " + myFile + ". Continuing..."
			print "Completed day " + str(days[d]) + " of year " + str(y)

def loadOtherVars():
	fileReader = open("daily_ISO-NE_2010-2014.csv", "rU")
	reader  = csv.DictReader(fileReader)
	gasDict = {}

	# gas data by day
	for row in reader:
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
		date = str(year)+str(month)+str(day)
		gasDict[date] = row['gas_p']
	fileReader.close()

	fileReader = open("hourly_data_2010-2014.csv", "rU")
	reader  = csv.DictReader(fileReader)	
	demDict = {}

	# demand data by hour
	for row in reader:
		demDict['Date'] = demDict['DEMAND']
	fileReader.close()
	return gasDict, demDict





if __name__ == '__main__':
	for year in xrange(2010,2015):
		make3DDataset(year)
		print "Completed year " + str(year)





