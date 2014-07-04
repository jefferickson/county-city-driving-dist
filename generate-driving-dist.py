#!/usr/bin/python3

import sqlite3, requests, sys, datetime


def google_driving_dist(orig_lat, orig_long, dest_lat, dest_long):
    """
    Implementation of: http://stackoverflow.com/questions/17267807/python-google-maps-driving-time
    Can only send 2500 requests per day
    """

    (orig_coords, dest_coords) = ((orig_lat, orig_long), (dest_lat, dest_long))

    #Get the distance from Google Maps API
    result = requests.get('http://maps.googleapis.com/maps/api/distancematrix/json',
                              params = {'origins': str(orig_coords),
                                        'destinations': str(dest_coords),
                                        'mode': 'driving',
                                        'language': 'en-EN',
                                        'sensor': 'false'})
    return result.json()['rows'][0]['elements'][0]['distance']['value'] / 1000


def fetch_one_dist(dbhandle):
    """
    Select one null distance, fetch the distance, and then update the table.
    Returns a tuple of the updated distance, total n, and remaining n.
    OR None if no more rows left to calculate.
    """

    cur = dbhandle.cursor()

    #How many rows left?
    cur.execute('SELECT COUNT(*) AS n_null FROM listing WHERE driving_distance IS NULL')
    (n_null, ) = cur.fetchone()

    #Exit if nothing more to do!
    if not n_null: return None

    #Select a row that doesn't yet have a driving_distance
    cur.execute('SELECT fips, city_id, city_lat, city_long, county_lat, county_long FROM listing WHERE driving_distance IS NULL LIMIT 1')
    (fips, city_id, city_lat, city_long, county_lat, county_long) = cur.fetchone()

    #Get the driving_distance from Google
    driving_distance = google_driving_dist(city_lat, city_long, county_lat, county_long)

    #Update the database
    cur.execute('UPDATE listing SET driving_distance = ? WHERE fips = ? AND city_id = ?', (driving_distance, fips, city_id))
    dbhandle.commit()

    #Now recall the data we just entered to ensure it is in the database
    cur.execute('SELECT county_name, state_name, city_name, driving_distance FROM listing WHERE fips = ? AND city_id = ?', (fips, city_id))
    (county_name, state_name, city_name, driving_distance) = cur.fetchone()

    #Now how many rows left?
    cur.execute('SELECT COUNT(*) AS n_null FROM listing WHERE driving_distance IS NULL')
    (n_null, ) = cur.fetchone()

    #How many rows total?
    cur.execute('SELECT COUNT(*) AS n_all FROM listing')
    (n_all, ) = cur.fetchone()

    #Return the fetched data
    return (county_name, state_name, city_name, driving_distance, n_null, n_all)


if __name__ == '__main__':

    #The database filename is an argument
    (database_filename, ) = sys.argv[1:] if sys.argv[1:] else sys.exit('ERROR: no database name')

    #Connect to the database, complete one row with a driving_distance
    try:
        dbhandle = sqlite3.connect(database_filename)
        dist_results = fetch_one_dist(dbhandle)
    except:
        print('SQL ERROR')
    finally:
        if dbhandle:
            dbhandle.close()

    if dist_results:
        (county_name, state_name, city_name, driving_distance, n_null, n_all) = dist_results
    else:
        sys.exit('No more rows left. We\'re done!')

    #Print the diag info
    print('%s %s, %s -> %s: %d (%i/%i remaining)' % (datetime.datetime.now(), county_name, state_name, city_name, driving_distance, n_null, n_all))