## County/City Driving Distance Dataset Creation

#### Author: Jeff Erickson `<jeff@erick.so>`
#### Date: 2014-07-04 (Updated: 2014-09-13)

### Introduction

This is a simple group of scripts to ultimately generate a dataset that has the driving distance (in KM, according to Google Maps API) between every county population centroid in the lower 48 and each major U.S. city with over 2 million people in its primary statistical area.

Update (2014-09-13): The dataset has been created and is available [here](https://raw.githubusercontent.com/jefferickson/county-city-driving-dist/master/datasets/county-city-driving-dist.csv).

### Instructions

The R script (`create-db.r`) generates a database with one row per large city/county center combination in the lower 48 states.

The Python script (`generate-driving-dist.py`), per run, finds a row in the database that doesn't yet have a distance calculated, calculates the distance, and then saves it back to the database. It is meant to be run repetitively (as a cron job, for example).

Here is a sample cron tab:  
```
* * * * * /path/to/python3 /path/to/generate-driving-dist.py /path/to/database.db >> /path/to/log  
*/2 * * * * /path/to/python3 /path/to/generate-driving-dist.py /path/to/database/db >> /path/to/log
```

The final product will be a complete SQL database with all of the distance information. I will post the final database to this repo once it is complete.

### Time Estimate

There are 102,597 combinations that need distances calculated. Google Maps API limits you to 2,500 queries a day, but because of the limitations of cron jobs, we will run 2160 per day. Therefore the estimated run time is 48 days.

Update (2014-09-13): The process began on 2014-07-04 and completed on 2014-08-21.

### References

County Density/Distance/Population Map. Erickson, Jeffrey P. 2014. [(link)](https://github.com/jefferickson/county-dendist-map)
