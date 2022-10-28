# This script cleans MBDF (mean distance between failures data) for the NYCT Subway, MNR, and LIRR

# Libraries
library(tidyverse)
library(lubridate)
library(rstudioapi)

# Set working directory to current file location
setwd(dirname(getActiveDocumentContext()$path))

# Read in data
sub_df = read_csv("../../data/00-raw-data/MTA_Subway_Mean_Distance_Between_Failures__Beginning_2015.csv")
other_df = read_csv('../../data/00-raw-data/lirr-metro-north-data/mta-lirr-and-metro-north-mean-distance-between-failures-beginning-2015-1.csv')

# Convert date columns to date format so dfs can be joined
sub_df$month <- paste0(sub_df$month, "-01")
sub_df$month <- as.Date(sub_df$month)
other_df$ServiceDate <- as.Date(other_df$ServiceDate,format="%m/%d/%Y")
# Rename column to allow for merging
names(sub_df)[1] = "ServiceDate"
names(sub_df)[2] = "FleetType"
names(other_df)[4] = "mdbf"
# Add Agency column to Subways data set
sub_df$Agency = "Subways"

# Subway DF has rows that are delineated by train car type, which are not used in this analysis, thus these rows are dropped.
sub_df <- sub_df[sub_df$FleetType=="FLEET",]

# MNR/LIRR DF has rows that are delineated by train car type, which are not used in this analysis, thus these rows are dropped.
# MNR values of FleetType are NA since all MNR entries are for their entire fleet in their given time frame, so these rows are filled in with FLEET
other_df$FleetType <- ifelse(other_df$Agency=="MNR","FLEET",other_df$FleetType)
other_df$FleetType <- ifelse(other_df$FleetType=="Entire Fleet","FLEET",other_df$FleetType)
other_df <- other_df[other_df$FleetType=="FLEET",]

# Merge dfs by all columns
df <- full_join(sub_df,other_df,by=c("ServiceDate","Agency","mdbf","FleetType"))

# Save to csv
write.csv(df,"../../data/01-modified-data/MDBF-Cleaned-Merged.csv")
                