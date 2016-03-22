/*clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_FULL_RESOURCES_2010.csv"
save set2010
clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_FULL_RESOURCES_2011.csv"
save set2011
clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_FULL_RESOURCES_2012.csv"
save set2012
clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_FULL_RESOURCES_2013.csv"
save set2013
clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_FULL_RESOURCES_2014.csv"
save set2014

use set2014
append using set2013
append using set2012
append using set2011
append using set2010

save set2010to2014
*/

/*
use set2010to2014
/*
save all the files 2010-2014 as .dta
then
use [dataset]
--> append using [other dataset that we have open]
*/

// drop if mwadded > 5000

gen demand_mwadded = mwadded*demand
gen gaspercentage100 = gaspercentage*100
gen mwadded2 = mwadded^2

reg netpricechange mwadded mwadded2 demand gaspercentage100 if demand > 16000, robust
reg netpricechange mwadded mwadded2 demand gaspercentage100 if demand < 10000, robust

scatter netpricechange mwadded if demand > 21300, title("Top 1% Demand, > 21300 MW")
scatter netpricechange mwadded if demand < 9230, title("Bottom 1% Demand, < 9230 MW")

*/
