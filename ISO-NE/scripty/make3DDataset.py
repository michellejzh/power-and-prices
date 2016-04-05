import csv
import os

def make3DDataset(year):
	writePath = "time-mw-price_"+str(year)+"_BY100.csv"
	with open(writePath, 'w') as fp:
		writer = csv.writer(fp, delimiter=',')
		writer.writerow(["Timestamp","MW Added","Price","Original Price","Demand","Temperature","Gas Percentage"])
		years = os.listdir("add-wind-prices")
		varDict = loadOtherVars()
		y = year

		days = os.listdir("add-wind-prices/" + str(year))
		for d in xrange(1,len(days)):
		# for d in xrange(1,2):
			hours = os.listdir("add-wind-prices/" + str(year) + "/" + days[d])
			for h in xrange(1,25):
				myFile = days[d] + "_" + str(h) + "_adjWindPrices.csv"
				# print "Opening file " + myFile
				try:
					fileReader = open("add-wind-prices/" + str(year) + "/" + days[d] + "/" + myFile, "rU")
					reader  = csv.DictReader(fileReader)
					done = 0
					count = 99
					originalPrice = -1
					for row in reader:
						if done == 0: # skip the first row
							done = 1
						else:
							count += 1
							# write 1 in every 100 lines
							if count % 100 == 0:
								if originalPrice == -1:
									originalPrice = float(row['Price'])
								if float(row['MW Wind Added']) > 5000.0:
									# print "More than 5 KW added. Breaking..."
									break
								pieces = myFile.split("_")
								myHour = int(pieces[1])
								if myHour < 10:
									myHour = "0" + str(myHour)
								timestamp = pieces[0] + str(myHour)
								writer.writerow([timestamp,int(float(row['MW Wind Added'])),row['Price'],originalPrice,varDict[pieces[0]][0],varDict[pieces[0]][1],varDict[pieces[0]][2]])
				except IOError:
					print "Failed to open file " + myFile + ". Continuing..."
			print "Completed day " + str(days[d]) + " of year " + str(y)

def loadOtherVars():
	fileReader = open("daily_ISONE_2010-2014.csv", "rU")
	reader  = csv.DictReader(fileReader)
	varDict = {}


	# need: DA_DEMD_AVG, DA_EC_AVG, DryBulb_avg, GAS
	# all by day
	count = 0
	for row in reader:
		count += 1
		print count
		try:
			if row['DATE'] == "":
				break
			date = row['DATE'].split('/')
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
			newRow = [row['DA_DEMD_AVG'],row['DryBulb_avg'],row['GAS_P']]
			varDict[date] = newRow
		except ValueError:
			print "Oops, ValueError on row " + str(row) + ". Continuing..."
	fileReader.close()
	return varDict





if __name__ == '__main__':
	# for year in xrange(2010,2014):
		year = 2010
		print "Beginning year " + str(year)
		make3DDataset(year)
		print "Completed year " + str(year)





