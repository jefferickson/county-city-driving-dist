## County/City Driving Distance Dataset and Map

#### Author: Jeff Erickson `<jeff@erick.so>`
#### Date: 2014-09-13

### Introduction

This is a dataset that has the driving distance (in km, according to Google Maps API) between every county population centroid in the lower 48 and each major U.S. city with over 2 million people in its primary statistical area.

For information on how this dataset was created, please see [this README](https://github.com/jefferickson/county-city-driving-dist/blob/master/README-creation.md).

### The Dataset

[The dataset](https://raw.githubusercontent.com/jefferickson/county-city-driving-dist/master/datasets/county-city-driving-dist.csv) contains 102,597 rows: one row per U.S. county (in the lower 48 states) per major U.S. city.

The variables include:

1. `fips`: the FIPS code of the county
2. `city_id`: the ID code of the city, as defined in [this key](https://raw.githubusercontent.com/jefferickson/county-city-driving-dist/master/datasets/maj.city.long.lat.csv)
3. `county_name`: the name of the county
4. `state_name`: the name of the state that the county is in
5. `county_lat`: the latitude of the population centroid of the county
6. `county_long`: the longitude of the population centroid of the county
7. `city_rank`: the rank of the population of the city
8. `city_name`: the name and state of the city
9. `city_long`: the longitude of the city
10. `city_lat`: the latitude of the city
11. `driving_distance`: the driving distance, in km, according to Google Maps API, between the city and the county population centroid
12. `shortest_flag`: a flag indicating if this is the closest city for each county population centroid

### Mapping the Results

To help visualize this data, here is a map of the z-score of the shortest driving distance for each county:

![Map of the shortest driving distances](https://raw.githubusercontent.com/jefferickson/county-city-driving-dist/master/map_output/map.v1.png)
[Large PDF](https://raw.githubusercontent.com/jefferickson/county-city-driving-dist/master/map_output/map.v1.pdf)

### Extension: Driving Distance and its Relation to Rurality

For more information on this topic, please see the [County Density/Distance/Population Map](https://github.com/jefferickson/county-dendist-map).