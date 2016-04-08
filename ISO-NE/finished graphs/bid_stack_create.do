clear
import delimited "/Users/Michelle/Desktop/power-and-prices/ISO-NE/scripty/longStack_20100101_hour8.csv", encoding(ISO-8859-1)
label var id "MW"
label var price "$/MW"
scatter price id, scheme(s1color) xline(13847) title("Merit order curve for 1/1/10, 9 AM")
