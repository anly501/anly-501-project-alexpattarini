library(tidyverse)
library(lubridate)
library(rstudioapi)

# Set working directory to current file location
setwd(dirname(getActiveDocumentContext()$path))

# Import MNR/LIRR On Time Performance Data
otp <- read_csv("../../data/00-raw-data/lirr-metro-north-data/mta-lirr-and-metro-north-on-time-performance-beginning-2015-1.csv")
# Import MNR/LIRR Delays/Reliability Data
delays <- read_csv("../../data/00-raw-data/lirr-metro-north-data/mta-lirr-and-metro-north-service-reliability-beginning-2015-1.csv")

# Split data frames by agency for easier merging later on
otp_mnr <- filter(otp,otp$Agency=="MNR")
otp_lirr <- filter(otp,otp$Agency=="LIRR")

delays_mnr <- filter(delays,delays$Agency=="MNR")
delays_lirr <- filter(delays,delays$Agency=="LIRR")

# Drop columns containing entirely missing (NA) values --- LIRR dataframes do not require this
otp_mnr <- otp_mnr[ , colSums(is.na(otp_mnr))==0]
delays_mnr <- delays_mnr[ , colSums(is.na(delays_mnr))==0]

# Drop rows with specific routes (creates duplicate rows if kept)
otp_mnr <- filter(otp_mnr,otp_mnr$`Branch / Line`=="System Total")
otp_lirr <- filter(otp_lirr,otp_lirr$`Branch / Line`=="System Total")

# AM Peak for OTP LIRR contains excessive number of missing values, and thus is dropped
otp_lirr <- select(otp_lirr,-"AM Peak")

# Join MNR and LIRR datasets respectively
mnr_ovr <- full_join(otp_mnr,delays_mnr,by=c("ServiceDate","Agency"))
lirr_ovr <- full_join(otp_lirr,delays_lirr,by=c("ServiceDate","Agency"))

# Type cast to date type --- All other columns are of correct data type
mnr_ovr$ServiceDate <-as.Date(mnr_ovr$ServiceDate, format="%m/%d/%Y")
lirr_ovr$ServiceDate <-as.Date(lirr_ovr$ServiceDate, format="%m/%d/%Y")


