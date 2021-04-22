I am interested in finding out if there is a relationship between the number of crimes reported, population and income.

NOTE 1:
About csv files. I could download csv manually, but when trying to use curl -o on oringal urls, the process failed. 
In order to follow the specifications of the ca1, I uploaded all csv files into a public and personal storage. 
In the following list, oringal (the original source from website cso Ireland) and csv file (personal and public link to storage).
All this process is located in ca1/initial_data.

LINKS:
Number of crimers per garda station per county: 
	original: https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/CJA07/CSV/1.0/en
	csv file: http://tanniestudio.com/mydata/CENSUS_2016_PRELIM_RESULTS.csv

Population sensor from 1984 to 2016: 
	original: https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/E2001/CSV/1.0/en/TLIST(A1)
	csv file: http://mydata.tanniestudio.com/E2001.Population.csv

Income per county from 2011 to 2019: 
	original: https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/CIA02/CSV/1.0/en
	csv file: http://mydata.tanniestudio.com/CIA02.Estimates%20of%20Household%20Income.csv

NOTE: there were some issues when downloading files using curl -o, to keep on with the process 
	of downloading file from url, i decided to save these files manually, uploaded them on my
	public repository space and download from my url.


Outcomes:
1) Number of crime offences recorded per county per year
2) Average household income per county per year
3) Population per county per year
4) Mapping total crime offences, income and population per county per year.
5) Mapping total crime offences, income and population per county.

NOTE 2: 
About normalise process.
It was detected that some columns in population and crime datasets were treated as variables instead of observations,
I used python to convert these columns quicker (I tried to find a process in sql, but I did not succeed). The python code
is located in ca1/normalise/transforming_data.py. After that, a new sql file was made to create again new initial_tables called this time
transformed_tables. Also load_verification was conducted. All this process is in folder ca1/normalise.


BREAKDOWN:
ca1.zip/
    README.txt  
    initial_data/
        data_download.sh  
        load_verification.sql
        load_verification.txt
        initial_tables.sql
        data_load.sql
        datasets/
           crime.csv
           county.csv
           income.csv
           popularion.csv
    normalise/
        transformed_tables.sql
        load_verification.sql
        load_verification.txt
        normalise.sql
        transforming_data.py
        load_transformed_data.sql
        queries.sql
	er_diagram.pdf
        datasets/
            crime_2.csv
            population_2.csv

NOTE 3: also, this is avaiable in server.
