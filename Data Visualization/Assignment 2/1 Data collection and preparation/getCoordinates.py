import sqlalchemy
import pandas as pd
import numpy as np
import geojson
import os


"""
    
    This file runs import to database all coordinates to draw the geofence on maps.+

"""

def start_getCoordinates_process():
    
    # SQL data --------------------------------------------------------------------------------
    
    """
    config = {
      'user': 'root',
      'password': 'k4Rl4#05',
      'host': 'localhost',
      'database': 'bikes',
    }
    """
    
    config = {
      'user': 'tanniest_mybikes',
      'password': 'WNZvC=M^u.pQ',
      'host': 'mx74.hostgator.mx',
      'database': 'tanniest_mybikes',
    }
    
    
    engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                            format(config['user'], config['password'], 
                                                   config['host'], config['database']))
    
    # -----------------------------------------------------------------------------------------
    
    
    # Import Dublin map. As no geofence was found, map was taken as a square ------------------
    coordinates = np.array([[-6.350928, 53.394139], 
                            [-6.082071, 53.394139], 
                            [-6.082071, 53.236784], 
                            [-6.350928, 53.236784]])
    
    coord = pd.DataFrame(coordinates, columns=['Longitude', 'Latitude']).reset_index()
    coord.columns = ['Id','Longitude', 'Latitude']
    coord.to_sql(con=engine, schema="tanniest_mybikes", name='dublinmap', if_exists='replace', index=False)
    
    # Import valid area for moby bikes -------------------------------------------------------
    filename = r'1 Data collection and preparation\Datasets\coordinates\mobybikes_map.geojson'   
    path_project = r'E:\Karla\IRELAND v2\DKIT\2nd Semester\Data Visualization\CA\CA2'

    with open(os.path.join(path_project, filename)) as f:
        gj = geojson.load(f)
    
    coord2 = np.array(gj['features'][-1]['geometry']['coordinates'][0])
    coord2 = pd.DataFrame(coord2, columns=['Longitude', 'Latitude']).reset_index()
    coord2.columns = ['Id','Longitude', 'Latitude']
    coord2.to_sql(con=engine, schema="tanniest_mybikes", name='mobyarea', if_exists='replace', index=False)


if __name__ == 'main':
    
    start_getCoordinates_process()
