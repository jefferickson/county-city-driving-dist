library(RSQLite)

### CONNECT TO SQLite DATABASE, IMPORT
db.handle <- dbConnect(dbDriver("SQLite"), dbname="database/county-city-listing.db")
county.city.list.long <- dbReadTable(db.handle, "listing")

### FIND SHORTEST DISTANCE FOR EACH COUNTY
county.city.shortest <- ddply(county.city.list.long, .(fips), function(x) {
  return(x[which.min(x$driving_distance), ])
})

### FLAG SHORTEST PER FIPS 
county.city.shortest$shortest_flag <- c(1)
county.city.list.long <- merge(county.city.list.long, county.city.shortest[c("fips", "city_id", "shortest_flag")], by=c("fips", "city_id"), all.x=TRUE)

### AND EXPORT
write.table(county.city.list.long, file="datasets/county-city-driving-dist.csv", sep=",", row.names=FALSE, col.names=TRUE)