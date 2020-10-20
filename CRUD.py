import psycopg2
import fire
from coolname import generate_slug

conn = psycopg2.connect(host="localhost", port = 5433, database="Prototype_Events", user="postgres", password="simplepassword")

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
