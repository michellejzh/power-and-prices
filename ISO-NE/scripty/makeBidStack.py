import csv
import os
import sys
import fileinput


def makeBidCurve():
	print "Opening file..."
	with open("/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/stacks/2010/20100101/20100101_hour8_bidStack.csv", 'rU') as csvfile:
		reader  = csv.DictReader(csvfile)
		countID = 0
		stacked = "longStack_20100101_hour8.csv"
		with open(stacked, 'w') as fp:
			print "Writing to file..."
			writer = csv.writer(fp, delimiter=',')
			writer.writerow(["ID", "Price"])	
			for row in reader:
				print "row!"
				price = row['Price']
				quantity = int(float(row['Quantity']))
				for i in xrange(quantity):
					countID += 1
					writer.writerow([countID,price])


if __name__ == '__main__':
	makeBidCurve()


