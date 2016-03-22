/*
clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_FULL_RESOURCES_2010.csv"
save set2010f
clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_FULL_RESOURCES_2011.csv"
save set2011f
clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_FULL_RESOURCES_2012.csv"
save set2012f
clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_FULL_RESOURCES_2013.csv"
save set2013f
clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/time-mw-price_FULL_RESOURCES_2014.csv"
save set2014f

use set2014f
append using set2013f
append using set2012f
append using set2011f
append using set2010f

save set2010to2014f, replace
*/
use set2010to2014f


// make sure there isn't overemphasis of the higher demand hours' tails

drop if mwadded > 5000

gen demand_mwadded = mwadded*demand
gen gaspercentage100 = gaspercentage*100
gen coalpercentage100 = coalpercentage*100
gen hydropercentage100 = hydropercentage*100
gen nuclearpercentage100 = nuclearpercentage*100

gen mwadded_gas = mwadded*gaspercentage100
gen mwadded_coal = mwadded*coalpercentage100
gen mwadded_hydro = mwadded*hydropercentage100
gen mwadded_nuclear = mwadded*nuclearpercentage100

gen mwadded2 = mwadded^2

gen mwadded2_gas = mwadded2*gaspercentage100
gen mwadded2_coal = mwadded2*coalpercentage100
gen mwadded2_hydro = mwadded2*hydropercentage100
gen mwadded2_nuclear = mwadded2*nuclearpercentage100

save set2010to2014f

//reg netpricechange mwadded mwadded2 demand gaspercentage100 coalpercentage100 hydropercentage100 nuclearpercentage100 mwadded_gas mwadded_coal mwadded_hydro mwadded_nuclear if demand > 23000
reg netpricechange mwadded_gas mwadded_coal mwadded_hydro mwadded_nuclear demand if demand > 23000
reg netpricechange mwadded_gas mwadded_coal mwadded_hydro mwadded_nuclear mwadded2_gas mwadded2_coal mwadded2_hydro mwadded2_nuclear demand if demand > 23000


//reg netpricechange mwadded mwadded2 demand gaspercentage100 if demand > 16000, robust
//reg netpricechange mwadded mwadded2 demand gaspercentage100 if demand < 10000, robust

//scatter netpricechange mwadded if demand > 21300, title("Top 1% Demand, > 21300 MW")
//scatter netpricechange mwadded if demand < 9230, title("Bottom 1% Demand, < 9230 MW")


