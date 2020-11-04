import atexit
from time import time, strftime, localtime
from datetime import timedelta, datetime
import random
from coolname import generate_slug
from geographiclib.constants import Constants
from geographiclib.geodesic import Geodesic
import csv

start = None
total = 0
loop_count = 0
t_elapsed = None


def start_log():
    global start
    if t_elapsed == None:
        start = time()


def end_log():
    global t_elapsed
    global loop_count

    t_elapsed = time() - start
    loop_count += 1

    print("End Loop {}, Execution time: {}".format(loop_count, t_elapsed))


def getEndpoint(lat1, lon1, d1, d2):
    bearing = random.uniform(0, 360)
    dist = random.uniform(d1, d2)
    radius = (d2-d1)/2
    geod = Geodesic(Constants.WGS84_a, Constants.WGS84_f)
    d = geod.Direct(lat1, lon1, bearing, dist)
    return d['lon2'], d['lat2'], radius


def generate_points(number: int, r1: float, r2: float):
    """
    Generate a number of coordinates
    :param number:  number of points
    :param r1:      min radius
    :param r2:      max radius   
    :return:        list of coordinates
    """
    lon = 18.865644     # Longitude of origin point
    lat = -33.930755    # Latitude of origin point
    points = []

    for _ in range(0, number):
        points.append(getEndpoint(lat, lon, r1, r2))

    return points


def generate_points_file(number: int, r1: float, r2: float, name: str):
    """
    Generate a number of coordinates
    :param number:  number of points
    :param r1:      min radius
    :param r2:      max radius   
    :param name:    name of output file
    :return:        outputs file with list of coordinates
    """
    lon = 18.865644     # Longitude of origin point
    lat = -33.930755    # Latitude of origin point
    points = []

    for _ in range(0, number):
        points.append(getEndpoint(lat, lon, r1, r2))

    with open('{}.csv'.format(name), 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Longitude', 'Latitude', 'Radius(m)'])
        for row in points:
            csv_out.writerow(row)

    return points


def event_create_file(min_dist: float, max_dist: float, num: int, name: str):
    """
    Generate a number of database entries within given radius bounds of set coordinates
    :param min_dist:      min radius in m
    :param max_dist:      max radius in m  
    :param num: number of points to generate
    :param name:    name of csv file
    :return: None
    """
    lon = 18.865644     # Longitude of origin point
    lat = -33.930755    # Latitude of origin point
    points = []

    for number, _ in enumerate(range(0, num), 1):

        # Create random coordinates within radius of distance provided
        lon2, lat2, _ = getEndpoint(lat, lon, min_dist, max_dist)

        # Generate random name
        event_name = generate_slug(2)

        points.append((event_name, lon2, lat2))

    with open('{}.csv'.format(name), 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Name', 'Longitude', 'Latitude'])
        for row in points:
            csv_out.writerow(row)

    return None
