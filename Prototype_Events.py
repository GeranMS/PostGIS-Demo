import psycopg2
import fire
from coolname import generate_slug
import CRUD
import Utilities
import atexit
from time import time, strftime, localtime
from datetime import timedelta

conn = psycopg2.connect(host="localhost", port = 5433, database="Prototype_Events", user="postgres", password="simplepassword")
#radius = 5000       # Distance in m
#lon = 18.865644     # Longitude of point 
#lat = -33.930755    # Latitude of point

def event_read_item(id: int):
    """
    Show event of given id 
    :param id:      id of event 
    :return:        Event details
    """

    atexit.register(Utilities.endlog)
    Utilities.log("Start Program")
    # Create a cursor object
    cur = conn.cursor()
    
    # Show table 'events' 
    cur.execute("SELECT (id,name,longitude,latitude) FROM events WHERE id=%s",[id])
    query_results = cur.fetchall()

    conn.commit()
    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()

    return print(query_results)

def event_delete_all():
    """
    Delete all events entries from events table
    :return:        None
    """
    # Create a cursor object
    cur = conn.cursor()

    # Add new entry into "events" table in the "Prototype_Events" database
    cur.execute("TRUNCATE TABLE events")
    cur.execute("ALTER SEQUENCE events_id_seq RESTART WITH 1")
    cur.execute("UPDATE events SET id=nextval('events_id_seq')")
   
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
    cur.execute("SELECT (id,name) FROM events WHERE ST_DWithin(coordinates, 'SRID=4326;POINT(%s %s)'::geography, %s)",(lon,lat,rad))
    query_results = cur.fetchall()

    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()

    return print(query_results)

def event_count(lon: float, lat: float, rad: float):
    """
    Query database and count events within given radius of coordinates
    :param lon: longitude of point
    :param lat: latitude of point
    :param rad: radius in m
    :return: count
    """

    atexit.register(Utilities.endlog)
    Utilities.log("Start Program")
    # Create a cursor object
    cur = conn.cursor()

    # A sample query of data within radius from the "events" table in the "Prototype_Events" database
    cur.execute("SELECT COUNT(id) FROM events WHERE ST_DWithin(coordinates, 'SRID=4326;POINT(%s %s)'::geography, %s)",(lon,lat,rad))
    query_results = cur.fetchall()

    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()

    return print(query_results[0][0])

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

    for num,points in enumerate(range(0,num),1):

        # Create random coordinates within radius of distance provided
        lon2,lat2 = Utilities.getEndpoint(lat,lon,min_dist,max_dist)

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
        "event_create":    CRUD.event_create,
        "event_read":    CRUD.event_read,
        "event_read_item":    event_read_item,
        "event_update_name":    CRUD.event_update_name,
        "event_update_loc":    CRUD.event_update_loc,
        "event_delete":    CRUD.event_delete,
        "event_delete_all":    event_delete_all,
        "event_count":    event_count,
        "event_create_random": event_create_random
    })

