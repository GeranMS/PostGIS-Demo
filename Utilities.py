import atexit
from time import time, strftime, localtime
from datetime import timedelta, datetime
import random
from geographiclib.constants import Constants
from geographiclib.geodesic import Geodesic

start=None

def secondsToStr(elapsed=None):
    if elapsed is None:
        global start
        start = time()
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        return str(timedelta(seconds=elapsed))

def log(s, elapsed=None):
    line = "="*40
    print(line)
    print(secondsToStr(), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()

def endlog():
    
    end = time()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))

""" start = time()
atexit.register(endlog)
log("Start Program") """

#
def getEndpoint(lat1, lon1, d1, d2):
    bearing = random.uniform(0,360)
    d = random.uniform(d1,d2)
    geod = Geodesic(Constants.WGS84_a, Constants.WGS84_f)
    d = geod.Direct(lat1, lon1, bearing, d)
    return d['lon2'], d['lat2']