clear
use resourceRegress

// do each resource separately
areg da_ec_avg coal_p coal_winter coal_spring coal_summer winter spring summer, a(year) r
areg da_ec_avg gas_p gas_winter gas_spring gas_summer winter spring summer, a(year) r
areg da_ec_avg hydro_p hydro_winter hydro_spring hydro_summer winter spring summer, a(year) r
areg da_ec_avg nuclear_p nuclear_winter nuclear_spring nuclear_summer winter spring summer, a(year) r
areg da_ec_avg oil_p oil_winter oil_spring oil_summer winter spring summer, a(year) r
areg da_ec_avg refuse_p refuse_winter refuse_spring refuse_summer winter spring summer, a(year) r
areg da_ec_avg solar_p solar_winter solar_spring solar_summer winter spring summer, a(year) r
areg da_ec_avg wind_p wind_winter wind_spring wind_summer winter spring summer, a(year) r


// summary statistics for resources by season
// egen seasons = cut(season), group(5)
// sort seasons
// by seasons: summarize coal gas hydro nuclear oil refuse solar wind

scatter da_ec_avg coal_p gas_p hydro_p nuclear_p oil_p refuse_p solar_p wind_p, scheme(s1color)
graph bar gas nuclear coal hydro refuse oil wind solar, ytitle("MW") scheme(s1color) stack over(year, relabel(1 "2010" 2 "2011" 3 "2012" 4 "2013" 5 "2014")) title("Supply in ISO-NE day-ahead market, 2010-2014")
graph bar gas nuclear coal hydro refuse oil wind solar, ytitle("MW") scheme(s1color) stack over(seasons, relabel(1 "Fall" 2 "Winter" 3 "Spring" 4 "Summer")) title("Supply in ISO-NE day-ahead market, by season")


// a monster that has all of the variables
// areg da_ec_avg coal_p coal_winter coal_spring coal_summer gas_p gas_winter gas_spring gas_summer hydro_p hydro_winter hydro_spring hydro_summer oil_p oil_winter oil_spring oil_summer nuclear_p nuclear_winter nuclear_spring nuclear_summer refuse_p refuse_winter refuse_spring refuse_summer solar_p solar_winter solar_spring solar_summer wind_p wind_winter wind_spring wind_summer winter spring summer, a(year) r


// scatter coal_p gas_p, scheme(s1color) title("Relationship between supply shares of coal and gas")
// by season: sum da_ec_avg 
