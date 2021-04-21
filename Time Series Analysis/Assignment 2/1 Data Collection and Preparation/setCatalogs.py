import pandas as pd

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
        
    
    def create_postgresql_engine():
        return sqlalchemy.create_engine('postgresql://{0}:{1}@{2}/{3}'.
                                        format(config['user'], config['password'], 
                                               config['host'], config['database']))
    
        
    def send_return_data(dataset, df, cols, query, table):
        
        df.to_sql(con=create_postgresql_engine(), schema="public", name=table, if_exists='append', index=False)
        
        # Select new IDs    
        df_db = pd.read_sql_query(sql=query, con=create_postgresql_engine())
        dataset = pd.merge(dataset, df_db, how='inner', on=cols)
        
        print(table + ' has been inserted.' + ' Shape:', dataset.shape)
        
        return dataset
    
    def send_data(df, table):        
        df.to_sql(con=create_postgresql_engine(), schema="public", name=table, if_exists='append', index=False)
                
        
    # Loading location dataset
    location = pd.read_csv(r'catalogs\uslocations.csv')
    print('uslocations dataset shape:', location.shape)
    
    # Insert country
    columns = ['country_name', 'country_code']
    country = location[columns].drop_duplicates().reset_index(drop=True)
    country.columns = ['name', 'code']
    query = 'SELECT id as country_id_db, name as country_name, code as country_code FROM country;'
    table = 'country'
    location = send_return_data(location, country, columns, query, table)
    del country
        
    # Insert states
    # query = "INSERT INTO state(name, abbrev, country_id) VALUES (%s, %s, %s);"
    columns = ['state_name','state_id', 'country_id_db']
    state = location[columns].drop_duplicates().reset_index(drop=True)
    state.columns = ['name', 'abbrev', 'country_id']
    query = "SELECT id as state_id_db, name as state_name, abbrev as state_id, country_id as country_id_db FROM state;"
    table = "state"
    location = send_return_data(location, state, columns, query, table)
    del state
        
    # Insert city
    # query = "INSERT INTO city(name, state_id) VALUES (%s, %s);"
    columns = ['city','state_id_db']
    city = location[columns].drop_duplicates().reset_index(drop=True)
    city.columns = ['name', 'state_id']
    query = "SELECT id as city_id_db, name as city, state_id as state_id_db FROM city;"
    table = 'city'
    location = send_return_data(location, city, columns, query, table)
    del city
    
    # Insert Time/Zone
    # query = "INSERT INTO public.timezones(name)	VALUES (%s);"
    columns = ['timezone']
    timezone = location[columns].drop_duplicates().reset_index(drop=True)
    timezone.columns = ['name']
    query = "SELECT id as timezone_id_db, name as timezone FROM timezones;"
    table = 'timezones'
    location = send_return_data(location, timezone, columns, query, table)    
    del timezone
        
    # Insert location
    # query = "INSERT INTO public.location(country_id, state_id, city_id, timezone_id) VALUES (%s, %s, %s, %s);"
    columns = ['country_id_db', 'state_id_db', 'city_id_db', 'timezone_id_db']
    location2 = location[columns].drop_duplicates().reset_index(drop=True).copy()
    location2.columns = ['country_id', 'state_id', 'city_id', 'timezone_id']
    query = "SELECT id as location_id_db, country_id as country_id_db, state_id as state_id_db, city_id as city_id_db, timezone_id as timezone_id_db FROM public.location;"
    table = 'location'
    location = send_return_data(location, location2, columns, query, table)
    del location2
    
    del location, columns, query, table    
    # ----------------------------------------------------------
    
    exchange = pd.read_csv(r'catalogs\exchanges.csv')
    exchange.fillna("", inplace=True)
    send_data(exchange, "exchange")
    print('exchange has been inserted. Shape:', exchange.shape)
         
    instrument = pd.read_csv(r'catalogs\instruments.csv')
    instrument.fillna("", inplace=True)    
    send_data(instrument, "instrument")
    print('instruments has been inserted. Shape:', instrument.shape)
        
    
if __name__ == '__main__':    
    start_process()
          