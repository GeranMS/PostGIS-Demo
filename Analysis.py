import fire
import Prototype_Events as PE
import Utilities as Util
import csv


class Searches(object):

    def search(self, lon=18.865644, lat=-33.930755, rad=5000):
        return PE.event_search(lon, lat, rad)

    def count(self, lon=18.865644, lat=-33.930755, rad=5000):
        return PE.event_count(lon, lat, rad)

class Pipeline(object):

    def __init__(self):
        self.search_result = Searches()

    def event_search(self, lon, lat, rad):
        
        return print(self.search_result.search(lon, lat, rad))

    def event_search_count(self, lon, lat, rad):
        
        return print(self.search_result.count(lon, lat, rad))

    def event_generate_search_file(self, number, r1, r2, name):
        Util.generate_points_file(number, r1, r2, name)

    def populate_database_file(self, r1, r2, num, name):
        Util.event_create_file(r1, r2, num, name)

    def event_search_generate(self, number, r1, r2):
        self.list = Util.generate_points(number, r1, r2)
        
        for point in self.list:
            return print(self.search_result.search(*point))

    def event_search_file(self, name):
        with open('{}.csv'.format(name)) as f:
            next(f)
            self.list=[tuple(line) for line in csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)]
        
        for point in self.list:
            return print(self.search_result.search(*point))

    def event_search_count_generate(self, number, r1, r2):
        self.list = Util.generate_points(number, r1, r2)
        
        for point in self.list:
            print(self.search_result.count(*point))
    
    def event_search_count_file(self, name):
        with open('{}.csv'.format(name),'r',newline='') as f:
            next(f)
            self.list=[tuple(line) for line in csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)]

        for point in self.list:
            print(self.search_result.count(*point))

if __name__ == "__main__":
        fire.Fire(Pipeline)
        