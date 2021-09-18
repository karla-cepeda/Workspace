import yfinance as yf

import pandas as pd
import numpy as np

import sqlalchemy

def start_process():   

    # SQL INFORMATION
    config = {
      'user': '', # Change
      'password': '', # Change
      'host': '', # Change
      'database': '', # Change
    }
    
    def create_postgresql_engine():
        return sqlalchemy.create_engine('postgresql://{0}:{1}@{2}/{3}'.
                                        format(config['user'], config['password'], 
                                               config['host'], config['database']))
    
    
    def get_data(query):
        # Select new IDs    
        df_ = pd.read_sql_query(sql=query, con=create_postgresql_engine())
        
        return df_
    
    query = "SELECT s.id, s.ticker FROM public.symbol s;"
    tickers = get_data(query)
    
    for i in np.arange(0, len(tickers)):
        
        symbol_id = tickers.loc[i,'id']
        ticker_name = tickers.loc[i,'ticker']
        ticker = yf.Ticker(ticker_name)    

        # Get historical data from stock selected
        data = ticker.history(period='max')
        
        # Cleaning process ....
        # We dont need dividends and stock splits as paypal does not do that
        data.drop(columns=['Dividends', 'Stock Splits'], inplace=True)
            
        # Apply frequency format
        # Missing values are Holidays, lets add previous value from 
        history = data.asfreq(freq='B', how='end')
        #print(history[history.Open.isna()].head())    
        
        # Lets fill missing dates with previus value.
        history = data.asfreq(freq='B', how='end', method='ffill')    
        
        # By exploring basic statistics, it seems data is ok
        history.describe()
        
        # Reset index and rename columns
        history.reset_index(inplace=True)
        history.columns = ['date_price', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']
        
        # Insert symbol id.
        history['symbol_id'] = symbol_id
        
        history.open_price = history.open_price.round(2)
        history.high_price = history.high_price.round(2)
        history.low_price = history.low_price.round(2)
        history.close_price = history.close_price.round(2)
        
        history.to_sql(con=create_postgresql_engine(), schema='public', name='daily_data', if_exists='append', index=False)


if __name__ == '__main__':    
    start_process()
