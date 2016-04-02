/*
//===Merge the datasets==============================================================

clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_2010_BY100.csv"
save set2010, replace
clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_2011_BY100.csv"
save set2011, replace
clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_2012_BY100.csv"
save set2012, replace
clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_2013_BY100.csv"
save set2013, replace
clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_2014_BY100.csv"
save set2014, replace

use set2014
append using set2013
append using set2012
append using set2011
append using set2010

save set2010to2014, replace
*/



//===Do the regression===============================================================
use set2010to2014

gen demand2 = demand^2
gen mwadded2 = mwadded^2
gen gaspercentage100 = gaspercentage*100


/* then need to make all the gas and demand quintiles and interact the terms */

