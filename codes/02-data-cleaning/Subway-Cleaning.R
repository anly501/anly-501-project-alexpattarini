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
#levels(as.factor(fares$station))

# Check for NA values in columns
colSums(is.na(fares))
# NA values found in 3 columns, will be dealt with in later analyses if they become pertinent
# Unnecessary columns dropped
fares <- select(fares,-contains("airtrain"))
fares <- select(fares,-contains("bus"))
fares <- select(fares,-contains("path"))

# Check data types of columns
str(fares)

# Type cast date columns to date type
fares$from_date <- as.Date(fares$from_date)
fares$to_date <- as.Date(fares$to_date)
#str(fares)
#sum(fares$full_fare)/colSums(Filter(is.numeric,fares))