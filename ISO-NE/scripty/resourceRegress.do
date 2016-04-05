clear
//import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/daily_ISONE_2010-2014.csv", encoding(ISO-8859-1)
//gen DATE = date(date, "MD20Y")

use meritRegress
twoway (scatter rt_ec_avg DATE) (scatter da_ec_avg DATE), ytitle("$/MW")
