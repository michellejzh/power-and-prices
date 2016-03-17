import csv
import os

def getHourlyPrice():
	writePath = "hourly_calc_prices_2010-2014.csv"
	with open(writePath, 'w') as fp:
		writer = csv.writer(fp, delimiter=',')
		writer.writerow(["Date","Hour","Price"])
		years = os.listdir("add-wind-prices")
		# print years
		for y in xrange(1,len(years)):
			days = os.listdir("add-wind-prices/" + years[y])
			# print days
			for d in xrange(1,len(days)):
				hours = os.listdir("add-wind-prices/" + years[y] + "/" + days[d])
				# print hours
				for h in xrange(1,25):
					myFile = days[d] + "_" + str(h) + "_adjWindPrices.csv"
					print "Opening file " + myFile
					try:
						fileReader = open("add-wind-prices/" + years[y] + "/" + days[d] + "/" + myFile, "rU")
						reader  = csv.DictReader(fileReader) 
						done = 0
						for row in reader:
							if done == 2:
								break
							if done == 0: # skip the first row
								done = 1
							else:
								pieces = myFile.split("_")
								writer.writerow([int(pieces[0]),int(pieces[1]),row['Price']])
								done = 2
					except IOError:
						print "Failed to open file " + myFile + ". Continuing..."


getHourlyPrice()