import yfinance as yf

import pandas as pd
import numpy as np

import psycopg2 as pg
import psycopg2.extras as pgextras
from psycopg2 import Error

import sqlalchemy

def start_process():
    
    # SQL INFORMATION
    config = {
      'user': 'postgres',
      'password': 'karla',
      'host': 'localhost',
      'database': 'karla',
    }
    
    def establish_postgresql_connection():
             
        return pg.connect(database=config['database'],
                          user=config['user'],
                          password=config['password'])
        
    
    def insert_row(insert_q, select_q, values):
        
        id_ = None
        
        try:
            conn = establish_postgresql_connection()
            cur = conn.cursor(cursor_factory=pgextras.DictCursor)
            
            cur.execute(insert_q, values)        
            
            conn.commit()
            
            cur.execute(select_q)
            
            id_ = cur.fetchone()[0]
            
            cur.close()
            conn.close()
            
        except (Exception, Error) as error:
            
            print("Error while connecting to PostgreSQL", error)
            
            if(conn):
                cur.close()
                conn.close()
        
        return id_


    def get_rows(select_q, values, columns):
        
        df_ = None
        
        try:
            conn = establish_postgresql_connection()
            cur = conn.cursor(cursor_factory=pgextras.DictCursor)
            
            cur.execute(select_q, values)
            
            data = cur.fetchall()
            
            cur.close()
            conn.close()
            
            df_ = pd.DataFrame(data, columns=columns)
            
        except (Exception, Error) as error:
            
            print("Error while connecting to PostgreSQL", error)
            
            if(conn):
                cur.close()
                conn.close()
        
        return df_
        

    def create_postgresql_engine():
        return sqlalchemy.create_engine('postgresql://{0}:{1}@{2}/{3}'.
                                        format(config['user'], config['password'], 
                                               config['host'], config['database']))
    

    def send_data(df, table):
        df.to_sql(con=create_postgresql_engine(), schema="public", name=table, if_exists='append', index=False)
        
        return None
        
    def get_data(query):
        # Select new IDs    
        df_ = pd.read_sql_query(sql=query, con=create_postgresql_engine())
        
        return df_
    
    
    # Just per stock
    
    symbols = pd.read_csv(r'catalogs\symbols.csv')
    symbols.fillna("", inplace=True)
    print('symbols dataset shape:', symbols.shape)
    
    for i in np.arange(0, len(symbols)):
        
        ticker_name = symbols.loc[i,'name']  
        instrument = symbols.loc[i,'instrument']
        
        print(ticker_name, instrument)
        
        ticker = yf.Ticker(ticker_name)
        
        name = ticker.info['shortName']     
        
        # Get exchange id
        query = "SELECT e.id FROM public.exchange e WHERE e.abbrev = %s;"
        exchange = ticker.info['exchange']
        exchange_id = get_rows(query, (exchange,), ['exchange_id']).loc[0,'exchange_id']
        
        # Get instrument id
        query = "SELECT i.id, i.belong_business FROM public.instrument i WHERE i.name = %s;"
        instrument_db = get_rows(query, (instrument,), ['instrument_id', 'belong_business'])
        instrument_id = instrument_db.loc[0,'instrument_id']
        belong_business = instrument_db.loc[0,'belong_business']
        
        location_id = 0
        sector = ""
        industry = ""
        website_url = ""
        
        if belong_business:            
            city = ticker.info['city'].lower()
            state = ticker.info['state'].lower()
            print(ticker_name, "located in", city, state)
            
            select_q = "SELECT ci.id AS city_id FROM public.city ci INNER JOIN public.timezones ti ON ci.timezone_id = ti.id INNER JOIN public.county cou ON ci.county_id = cou.id INNER JOIN public.state s ON cou.state_id = s.id INNER JOIN public.country co ON s.country_id = co.id WHERE LOWER(ci.name) = %s AND LOWER(s.abbrev) = %s"
            values = (city, state)
            location = get_rows(select_q, (city, state), ["city_id"])
            location_id = location.loc[0,'city_id']
            
            if "sector" in ticker.info:
                sector = ticker.info['sector']
                industry = ticker.info['industry']
                website_url = ticker.info['website']
    
            insert_q = "INSERT INTO business(name, city_id, sector, industry, website_url)	VALUES (%s, %s, %s, %s, %s);"
            select_q = "SELECT id FROM business;"
            values = (name, int(location_id), sector, industry, website_url )
            business_id = insert_row(insert_q, select_q, values)
            print("business data inserted.")
    
        # Symbol information
        currency = ticker.info['currency']
        insert_q = "INSERT INTO symbol(exchange_id, ticker, instrument_id, currency) VALUES (%s, %s, %s, %s);"
        select_q = "SELECT id FROM symbol ORDER BY id DESC;"
        values = (int(exchange_id), ticker_name, int(instrument_id), currency)
        symbol_id = insert_row(insert_q, select_q, values)
        
        if location_id > 0:
            insert_q = "INSERT INTO public.symbol_business(symbol_id, business_id) VALUES (%s, %s);"
            select_q = "SELECT symbol_id, business_id FROM symbol_business;"
            values = (int(symbol_id), int(business_id))
            number = insert_row(insert_q, select_q, values)            
            print('symbol-business inserted')
           
        print("new stock inserted with id", symbol_id)
    
    
if __name__ == '__main__':
    start_process()
          