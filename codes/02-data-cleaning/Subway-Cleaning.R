library(tidyverse)
library(lubridate)
library(rstudioapi)

# Set working directory to current file location
setwd(dirname(getActiveDocumentContext()$path))

# Import fare card data set
fares <- read.csv("../../data/00-raw-data/MTA-Fare-Card-Data-From-2010.csv",row.names=1)

# Remove rows containing bus stop names, depot names, and PATH station names
fares <- filter(fares,!startsWith(fares$station,"PA-"))
fares <- filter(fares,!startsWith(fares$station,"SBS-"))
fares <- filter(fares,!endsWith(fares$station,"DEPOT"))
# Remove specific rows with station names not relevant to analysis
fares <- filter(fares,fares$station!="UNUSED")
fares <- filter(fares,fares$station!="MTABC - EASTCHESTER 2")
fares <- filter(fares,fares$station!="ORCHARD BEACH")
#levels(as.factor(fares$station))

# Check for NA values in columns
colSums(is.na(fares))
fares <- fares[ , colSums(is.na(fares)) == 0]
# Drop NA columns
# NA values found in 3 columns, will be dealt with in later analyses if they become pertinent
# Unnecessary columns dropped
fares <- select(fares,-contains("airtrain"))
fares <- select(fares,-contains("bus"))
fares <- select(fares,-contains("path"))

# Check data types of columns
#str(fares)

# Type cast date columns to date type
fares$from_date <- as.Date(fares$from_date)
fares$to_date <- as.Date(fares$to_date)
#str(fares)

# Remove duplicates if any
fares <- fares[!duplicated(fares),]

# Gather fares to longer format
fares_gathered <- gather(fares,fare_type,fare_count,-from_date,-to_date,-remote_station_id,-station)

# Remove column
fares_gathered <- fares_gathered[-4]

# Save gathered fares to csv
write.csv(fares_gathered,"../../data/01-modified-data/MTA-Fare-Card-Cleaned-Gathered.csv")