def orderByDemand():
	sort demand from lowest to highest hour
	then make a giant file where 
		1st column is the quantity of wind added
		2nd - last columns are all the prices resulting from the changed wind
			go from the lowest demand hour in col 2 to the highest demand hour in col n

		this will involve getting the dates of the files and putting them in year-mo-da format
		use the format to get the corresponding demand and bid stack hour files
			format: DATE_hr_adjustedWindPrices