import csv
import sys
import os

def cutHeader(myFile):
	if "TRIM" in myFile:
		return
	print "Opening", myFile
	with open(myFile, 'rU') as csvfile:
		r = csv.reader(csvfile, dialect=csv.excel_tab, delimiter=',', quotechar='|')
		fileSeg = myFile.split('/')

			writePath = fileSeg[0] + "/TRIM_" + fileSeg[1]
			with open(writePath, 'w') as fp:
				w = csv.writer(fp, delimiter=',')
				count = 0
				for row in r:
					# print count
					# print row
					count += 1
					if count > 4 and count != 6:
						# print row
						if row[0] == '"T"':
							break
						currRow = [row[1].replace('"',''), row[2].replace('"',''), row[3].replace('"','')]
						w.writerow(currRow) #write the 5th line
						# print row
				print "Wrote file " + str(myFile)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		try:
			folder = str(sys.argv[1])
		except ValueError:
			print "Error: input must be a string"
			exit()
	else:
		print "Usage: getDemands.py <cleared demand folder>"

	print "Folder: " + str(folder)
	files = os.listdir(folder)
	print "Files: " + str(files)
	numFiles = len(files)
	for i in xrange(numFiles):
		path = folder + "/" + files[i]
		cutHeader(path)







# def cutHeader(myFile):
# 	print "Opening", myFile
# 	with open(myFile, 'rU') as csvfile:
# 		r = csv.DictReader(csvfile)
# 		fileSeg = myFile.split('/')
# 		writePath = fileSeg[0] + "/TRIM_" + fileSeg[1]
# 		with open(writePath, 'w') as fp:
# 			w = csv.writer(fp, delimiter=',')
# 			count = 0
# 			for row in r:
# 				# print count
# 				# print row
# 				count += 1
# 				if count >= 4 and count != 6:
# 					currRow = [row['Date']]
# 					dataCol = row["['Hour Ending', 'Day-Ahead Cleared Demand']"]
# 					currRow.append(dataCol[0])
# 					currRow.append(dataCol[1])
# 					w.writerow(currRow) #write the 5th line
# 					# print row
# 			print "Rewrote file " + str(myFile)

