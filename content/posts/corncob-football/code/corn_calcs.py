mill = 1000000
bill = mill * 1000

iowa_prod = 2.7 * bill
iowa_acre_all = 13.5 * mill
iowa_acre_sweet = 3400

sweet_perc = iowa_acre_sweet / iowa_acre_all
sweet_bush = iowa_prod * sweet_perc
sweet_pounds = sweet_bush * 56

sweet_ears = sweet_pounds / 0.615
print("Number of ears of sweet corn produced in Iowa annually:")
print(sweet_ears)
