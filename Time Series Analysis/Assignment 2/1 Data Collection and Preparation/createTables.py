
import psycopg2 as pg
import psycopg2.extras as pgextras
from psycopg2 import Error


def start_process():
    
    # SQL INFORMATION
    config = {
      'user': '', # Change
      'password': '', # Change
      'host': '', # Change
      'database': '', # Change
    }
    
    
    def establish_postgresql_connection():
             
        return pg.connect(database=config['database'],
                          user=config['user'],
                          password=config['password'])
        
    
    try:
        conn = establish_postgresql_connection()
        cur = conn.cursor(cursor_factory=pgextras.DictCursor)
        
        cur.execute(open("sql\initial_tables.sql", "r").read())       
        
        conn.commit()
                    
        cur.close()
        conn.close()
            
    except (Exception, Error) as error:
        
        print("Error while connecting to PostgreSQL", error)
        
        if(conn):
            cur.close()
            conn.close()
        

if __name__ == '__main__':    
    start_process()
          