# PostGIS-Demo
_This is an example on how to integrate and implement basic CRUD and location add/search functionality with Python and a PostGIS enabled PostgreSQL database._

## Installation

1. Download or clone this project and use provided virtual environment called 'env' for supporting libraries.
1. Download or clone this project but install additional libraries yourself from the requirements.txt.

    #### Quick 'How to' on installing from requirements.txt
    * Make sure you are in the project folder and run the following command in your terminal: 
      `pip install -r requirements.txt`
      
## Setup

To intitialize a PostGIS enabled PostgreSQL database follow the guide posted in the docs folder linked to [here](https://github.com/GeranMS/PostGIS-Demo/tree/master/docs).

Then configure and change your connection string to your specifications of the database in the code of Prototype_Events.py and CRUD.py, as shown an example of here:
~~~python
conn = psycopg2.connect(host="localhost", port = 5433, database="Prototype_Events", user="postgres", password="simplepassword")
~~~

Then change all reference to 'event' and 'coordinates' in the SQL code to your table name and geography column as initialized above.

## The Program CLI

The CLI was developed with the python module, [fire](https://github.com/google/python-fire), and was used to develop a user-friendly console application. To find the list and explanation of all the commands available, use the --help command as follows:
`python Prototype_Events.py --help`

## Basic Usage(event_create_random):

If you want to populate the database with a number of data points(locations) you would use the, event_create_random, command. e.g Create a 1000 points in a radius from 5000m to 10000m from a location(18.865644 -33.930755) as follows:

`python Prototype_Events.py event_create_random --lon 18.865644 --lat -33.930755 --min_dist 5000 --max_dist 10000 --num 1000`

## Commands Reference

All of the commands referenced below is can be found in the program CLI by the --help command.

|Command            |Inputs                                       |Outputs              |Notes                                                                                |
|-                  |-                                            |-                    |-                                                                                    |
|event_create       |--name, --lon, --lat                         |None                 |Add a new entry to the configured table                                              | 
|event_read         |None                                         |List of all entries  |Shows the table as configured                                                        |
|event_read_item    |--id                                         |Entry                |Shows the table as configured                                                        |
|event_update_name  |--id, --name                                 |None                 |Update an entry's name                                                               |
|event_update_loc   |--id, --lon, --lat                           |None                 |Update an entry's location                                                           |
|event_delete       |--id                                         |None                 |Delete an entry from configured table                                                | 
|event_delete_all   |None                                         |None                 |Delete all entries from configured table                                             |
|event_create_random|--lon, --lat, --min_dist, --max_dist, --num  |None                 |Generate a number of database entries within given radius bounds of given coordinates|
|event_search       |--lon, --lat, --rad                          |List of entries      |Query database for entries within given radius of coordinates given                  |
|event_count        |--lon, --lat, --rad                          |Count of points      |Query database for entries within given radius of coordinates given                  |
