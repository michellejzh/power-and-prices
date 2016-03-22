import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/hourly_data_2010-2014_CUT.csv"
sum daenergycost
sum meritorderprice
gen price_diff = daenergycost - meritorderprice
sum price_diff
reg price_diff drybulb demand da_cc da_mlc
