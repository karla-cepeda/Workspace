Student name: Karla Aniela Cepeda Zapata
Student ID: d00242569

The database used was PostgreSQL, in local instance (student's computer).

Run python file setup.py. This will create and import all the data needed by accessing to other python files. These files are:
- setBussinesData.py
- setCatalogs.py
- setHistoricalStockData.py
- createTables.py

Requirements:
python version => 3.8.3
psycopg2 => 2.8.6
yfinance => 0.1.55
pandas => 1.0.5
numpy => 1.18.5
sqlalchemy => 1.3.18


NOTE 1: I tried to run setup.py on shared server, however I got an error: Pandas module does not exist. Therefore, I decided to work locally.

NOTE 2: project available in private git repository. Request for access if it is needed.
https://github.com/karla-cepeda/Workspace/tree/master/Data%20Architecture/Assignment%202

NOTE 3: in the dataset it is included more tickers, but in Time Series Analysis Module I focused my analysis on PayPal Stock (ticker: PYPL). Therefore, for this CA i focused on PayPal too.