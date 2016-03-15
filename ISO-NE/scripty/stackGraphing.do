// clear
// import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/add-wind-prices/20120301_2_adjWindPrices.csv"
// twoway line price mwwindadded
graph twoway (line price mwwindadded) (fpfit price mwwindadded)
// graph twoway (scatter musttakeenergy segment1price if fuel_type==1) (scatter musttakeenergy segment1price if fuel_type==2) (scatter musttakeenergy segment1price if fuel_type==3) (scatter musttakeenergy segment1price if fuel_type==4) (scatter musttakeenergy segment1price if fuel_type==5), legend(label(1 one) label(2 two) label(3 three) label(4 four) label(5 five)) 
