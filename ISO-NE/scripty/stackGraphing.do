clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/add-wind-prices/2011/20110109/20110109_20_adjWindPrices.csv"
twoway line price mwwindadded
//graph twoway (line price mwwindadded) (fpfit price mwwindadded)
