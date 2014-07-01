### Adapted from: https://github.com/jefferickson/county-dendist-map/blob/master/county_dendist_map.Rmd

### LOAD LIBRARIES ###
library(RSQLite)
library(rgdal)

### IMPORT DATA ###

#County Shapes from US Census
county.shapes <- readOGR(dsn="datasets", "gz_2010_us_050_00_500k")

#County population centroids from US Census
county.pop.center <- read.csv("datasets/CenPop2010_Mean_CO.txt", header=TRUE)

#Major city (primary statistical areas) from gen.maj.city.long.lat.Rmd
maj.city.long.lat <- read.csv("datasets/maj.city.long.lat.csv", header=TRUE)

### DATA MANIPULATION ###

#Create full FIPS code
county.pop.center$GEO_ID <- paste("0500000US", formatC(county.pop.center$STATEFP, width=2, flag="0"), formatC(county.pop.center$COUNTYFP, width=3, flag="0"), sep="")

#Remove AK, HI, PR (2 codes)
county.pop.center <- county.pop.center[which(! (substr(county.pop.center$GEO_ID, 10, 11) %in% c("02", "52", "15", "72"))), ]

#Create a list of all unique combinations of counties and the major cities, remove and rename as necessary
county.city.list.long <- merge(county.pop.center, maj.city.long.lat, all.x=TRUE, all.y=TRUE)
county.city.list.long$STATEFP <- NULL
county.city.list.long$COUNTYFP <- NULL
county.city.list.long$POPULATION <- NULL
names(county.city.list.long) <- c("county_name", "state_name", "county_lat", "county_long", "fips", "city_id", "city_rank", "city_name", "city_long", "city_lat")

#Finally, we should create the field that will store the distances (which are NA for now)
county.city.list.long$driving_distance <- c(NA)

### CREATE SQLite DATABASE ###
db.handle <- dbConnect(dbDriver("SQLite"), dbname="database/county-city-listing.db")

dbWriteTable(db.handle, "listing", county.city.list.long, row.names=FALSE)