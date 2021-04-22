#!/bin/bash

# curl will download the URL given to the output file
# first two files are loacted in my public website since I could not download csv from original in bash
#  for more information, read README.txt in folder ca1.

curl -o "initial_data/datasets/crime.csv" "http://mydata.tanniestudio.com/CJA07.Recorded%20Crime%20Offences%20Ireland.csv"
curl -o "initial_data/datasets/population.csv" "http://mydata.tanniestudio.com/E2001.Population.csv"
curl -o "initial_data/datasets/income.csv" "http://mydata.tanniestudio.com/CIA02.Estimates%20of%20Household%20Income.csv"
curl -o "initial_data/datasets/county.csv" "http://mydata.tanniestudio.com/county.csv"
