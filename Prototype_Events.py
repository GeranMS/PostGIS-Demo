import psycopg2
import fire
from geographiclib.constants import Constants
from geographiclib.geodesic import Geodesic
import random
from coolname import generate_slug

conn = psycopg2.connect(host="localhost", port = 5433, database="Prototype_Events", user="postgres", password="simplepassword")
#radius = 5000       # Distance in m
#lon = 18.865644     # Longitude of point 
#lat = -33.930755    # Latitude of point

def event_create(name: str, lon: float, lat: float):
    """
    Add a new event entry into events table
    :param name:    name of event   
    :param lon:     longitude of point
    :param lat:     latitude of point
    :return:        None
    """
    # Create a cursor object
    cur = conn.cursor()
    # Create a cursor object
    cur2 = conn.cursor()

    # Add new entry into "events" table in the "Prototype_Events" database
    cur.execute("INSERT INTO events (name,longitude,latitude) VALUES (%s,%s,%s)",(name,lon,lat))
    # Create geometry column value off new entry 
    cur2.execute("UPDATE events SET coordinates=ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)")

    conn.commit()
    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    cur2.close()
    conn.close()

    return None

def event_read():
    """
    Show events table  
    :return:        None
    """
    # Create a cursor object
    cur = conn.cursor()
    
    # Show table 'events' 
    cur.execute("SELECT * FROM events")
    query_results = cur.fetchall()

    conn.commit()
    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()

    return print(query_results)

def event_update_name(id: int, name: str):
    """
    Update a event name from events table
    :param id:      id of event
    :param name:    name of event   
    :return:        None
    """
    # Create a cursor object
    cur = conn.cursor()
    
    # Update name of event selected by id 
    cur.execute("UPDATE events SET name=%s WHERE id=%s",(name,id))

    conn.commit()
    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()

    return None

def event_update_loc(id: int, lon: float, lat: float):
    """
    Update a event location from events table
    :param id:      id of event
    :param lon:     longitude of point
    :param lat:     latitude of point   
    :return:        None
    """
    # Create a cursor object
    cur = conn.cursor()
    # Create a cursor object
    cur2 = conn.cursor()
    
    # Update name of event selected by id 
    cur.execute("UPDATE events SET longitude=%s,latitude=%s WHERE id=%s",(lon,lat,id))
     # Create geometry column value off new entry 
    cur2.execute("UPDATE events SET coordinates=ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)")

    conn.commit()
    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    cur2.close()
    conn.close()

    return None

def event_delete(id: int):
    """
    Delete an event entry from events table
    :param id:      id of event
    :return:        None
    """
    # Create a cursor object
    cur = conn.cursor()

    # Add new entry into "events" table in the "Prototype_Events" database
    cur.execute("DELETE FROM events VALUES WHERE id=%s",[id])
   
    conn.commit()
    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()

    return None


def event_search(lon: float, lat: float, rad: float):
    """
    Query database for events within given radius of coordinates
    :param lon: longitude of point
    :param lat: latitude of point
    :param rad: radius in m
    :return: events
    """
    # Create a cursor object
    cur = conn.cursor()

    # A sample query of data within radius from the "events" table in the "Prototype_Events" database
    cur.execute("SELECT (id,name) FROM events WHERE ST_DWithin(coordinate, 'SRID=4326;POINT(%s %s)'::geography, %s)",(lon,lat,rad))
    query_results = cur.fetchall()

    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()

    return print(query_results)

def getEndpoint(lat1, lon1, d1, d2):
    bearing = random.uniform(0,360)
    d = random.uniform(d1,d2)
    geod = Geodesic(Constants.WGS84_a, Constants.WGS84_f)
    d = geod.Direct(lat1, lon1, bearing, d*1.852)
    return d['lon2'], d['lat2']

def event_create_random(lon: float, lat: float, min_dist: float, max_dist: float, num: int):
    """
    Generate a database entry within given radius of coordinates
    :param lon: longitude of point
    :param lat: latitude of point
    :param rad: radius in m
    :param num: number of points to generate
    :return: None
    """
    # Create a cursor object
    cur = conn.cursor()
    # Create a cursor object
    cur2 = conn.cursor()

    for num,point in enumerate(range(0,num),1):

        # Create random coordinates within radius of distance provided
        lon2,lat2 = getEndpoint(lat,lon,min_dist,max_dist)

        # Generate random name
        name = generate_slug(2)

        # Add new entry into "events" table in the "Prototype_Events" database
        cur.execute("INSERT INTO events (name,longitude,latitude) VALUES (%s,%s,%s)",(name,lon2,lat2))
        # Create geometry column value off new entry 
        cur2.execute("UPDATE events SET coordinates=ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)")

        if (num%100 == 0):
            
            conn.commit()
            print("%s Records have been inserted.\n"%(num))

    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    cur2.close()
    conn.close()

    return None

if __name__ == "__main__":
    fire.Fire({
        "event_search": event_search,
        "event_create":    event_create,
        "event_read":    event_read,
        "event_update_name":    event_update_name,
        "event_update_loc":    event_update_loc,
        "event_delete":    event_delete,
        "event_create_random": event_create_random
    })

