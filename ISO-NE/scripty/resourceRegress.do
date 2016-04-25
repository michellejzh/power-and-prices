clear
use resourceRegress

/*
// do each resource separately
eststo: quietly areg da_ec_avg coal_p coal_winter coal_spring coal_summer winter spring summer, a(year) r
eststo: quietly areg da_ec_avg gas_p gas_winter gas_spring gas_summer winter spring summer, a(year) r
eststo: quietly areg da_ec_avg hydro_p hydro_winter hydro_spring hydro_summer winter spring summer, a(year) r
eststo: quietly areg da_ec_avg nuclear_p nuclear_winter nuclear_spring nuclear_summer winter spring summer, a(year) r
eststo: quietly areg da_ec_avg oil_p oil_winter oil_spring oil_summer winter spring summer, a(year) r
eststo: quietly areg da_ec_avg refuse_p refuse_winter refuse_spring refuse_summer winter spring summer, a(year) r
eststo: quietly areg da_ec_avg solar_p solar_winter solar_spring solar_summer winter spring summer, a(year) r
eststo: quietly areg da_ec_avg wind_p wind_winter wind_spring wind_summer winter spring summer, a(year) r
esttab
*/

// summary statistics for resources by season
// egen seasons = cut(season), group(5)
// sort seasons
// by seasons: summarize coal gas hydro nuclear oil refuse solar wind

/*
scatter da_ec_avg coal_p gas_p hydro_p nuclear_p oil_p refuse_p solar_p wind_p, scheme(s1color)
graph bar gas nuclear coal hydro refuse oil wind solar, ytitle("MW") scheme(s1color) stack over(year, relabel(1 "2010" 2 "2011" 3 "2012" 4 "2013" 5 "2014")) title("Supply in ISO-NE day-ahead market, 2010-2014")
graph bar gas nuclear coal hydro refuse oil wind solar, ytitle("MW") scheme(s1color) stack over(seasons, relabel(1 "Fall" 2 "Winter" 3 "Spring" 4 "Summer")) title("Supply in ISO-NE day-ahead market, by season")
*/

// a monster that has all of the variables
// areg da_ec_avg coal_p coal_winter coal_spring coal_summer gas_p gas_winter gas_spring gas_summer hydro_p hydro_winter hydro_spring hydro_summer oil_p oil_winter oil_spring oil_summer nuclear_p nuclear_winter nuclear_spring nuclear_summer refuse_p refuse_winter refuse_spring refuse_summer solar_p solar_winter solar_spring solar_summer wind_p wind_winter wind_spring wind_summer winter spring summer, a(year) r


// scatter coal_p gas_p, scheme(s1color) title("Relationship between supply shares of coal and gas")
// by season: sum da_ec_avg 

// scatter da_ec_avg DATE, scheme(s1color) ytitle("Day-ahead daily average price, $") tlabel(01jan2010 01jan2011 01jan2012 01jan2013 01jan2014 01jan2015, format(%tdn/y))
//twoway (scatter da_demd_avg DATE, msymbol(oh) scheme(s1color) xtitle("Date") ytitle("MW") tlabel(01jan2010 01jan2011 01jan2012 01jan2013 01jan2014 01jan2015, format(%tdn/y)) ttick(01jul2010 01jul2011 01jul2012 01jul2013 01jul2014, format(%tdn/y)) title("Seasonal variation in demand and price") yaxis(1)) (scatter da_ec_avg DATE, msymbol(oh) yaxis(2) ytitle("$", axis(2)))

// schematic supply-demand diagram
// twoway (function y=(1/2)*2^(15*x)), title("Supply and demand in the day-ahead market") ylabel(none) xtitle(MW) ytitle($/MW) scheme(s1color) xline(0.55) xlabel(none)
/*
areg da_ec_avg coal_p da_demd_avg, a(seasonYear) r
areg da_ec_avg gas_p da_demd_avg, a(seasonYear) r
areg da_ec_avg hydro_p da_demd_avg, a(seasonYear) r
areg da_ec_avg nuclear_p da_demd_avg, a(seasonYear) r
areg da_ec_avg oil_p da_demd_avg, a(seasonYear) r
areg da_ec_avg refuse_p da_demd_avg, a(seasonYear) r
areg da_ec_avg solar_p da_demd_avg, a(seasonYear) r
areg da_ec_avg wind_p da_demd_avg, a(seasonYear) r

areg da_ec_avg coal_p hydro_p nuclear_p oil_p refuse_p solar_p wind_p da_demd_avg, a(seasonYear) r
areg da_ec_avg gas_p gas_winter gas_spring gas_summer winter spring summer da_demd_avg gas_spot_price, a(year) r
areg da_ec_avg wind_p wind_winter wind_spring wind_summer winter spring summer da_demd_avg gas_spot_price, a(year) r


twoway (scatter da_ec_avg wind_p if winter==0) (scatter da_ec_avg wind_p if winter==1), scheme(s1color) title("% of supply from wind vs. clearing price") legend(label(1 "Non-winter") label(2 "Winter")) xtitle("% of supply from wind") ytitle("Clearing price, $/MW")
*/
