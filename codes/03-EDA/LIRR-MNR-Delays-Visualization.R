library(tidyverse)
library(lubridate)
library(rstudioapi)

# Set working directory to current file location
setwd(dirname(getActiveDocumentContext()$path))

# Import LIRR and MNR reliability data sets
lirr <- read.csv("../../data/01-modified-data/LIRR-overall-delays-otp.csv",row.names = 1)
mnr <- read.csv("../../data/01-modified-data/MNR-overall-delays-otp.csv",row.names = 1)

### TIME SERIES ###

# Typecast date to date type
lirr$ServiceDate <- as.Date(lirr$ServiceDate,"%m/%d/%Y")
mnr$ServiceDate <- as.Date(mnr$ServiceDate, "%Y-%m-%d")

# Subset LIRR to relevant columns and group by OTP percentages for LIRR
lirr_g <- pivot_longer(lirr,c(OTP,PM.Peak,OffPeak))
lirr_g <- lirr_g[c("ServiceDate","Agency","Branch...Line","X4mTo6mTrainDelays","MajorIncidents","name","value")]
lirr_g <- lirr_g %>% rename("OTP"="value")
lirr_g$name <- ifelse(lirr_g$name=="OTP","Overall",ifelse(lirr_g$name=="PM.Peak","PM Peak","Off Peak"))
# Scale to range MNR Major Incidents to fit on time series plot
# Max scaled to 1, minimum is 0 so remains at 0
lirr_g$MajorIncidentsScaled <- lirr_g$MajorIncidents/max(lirr_g$MajorIncidents)

# LIRR time series ggplot
lirr_ts <- ggplot(data=lirr_g,aes(x=ServiceDate,y=OTP,group=name,color=name)) +
  geom_line() +
  scale_y_continuous(name="On Time Percentage",expand=c(0,0),labels=scales::percent) +
  scale_x_date(name="Date",date_breaks = "1 year",expand=c(0,0)) + 
  scale_color_discrete(name="Time Frame") +
  labs(title="LIRR On Time Percentage\n by Time Frame (2015-2022)") + 
  theme_bw() +
  theme(axis.text.x = element_text(angle=45,vjust=1,hjust=1))
lirr_ts
ggsave("../../501-project-website/images/TIMESERIES-LIRR-OTP.png")

# Scale to range MNR Major Incidents to fit on time series plot
# Max scaled to 1, minimum is 0 so remains at 0
mnr$MajorIncidentsScaled <- mnr$MajorIncidents/max(mnr$MajorIncidents)
# MNR time series ggplot
mnr_ts <- ggplot(data=mnr,aes(x=ServiceDate,y=OTP)) +
  geom_line(color="purple") +
  geom_bar(aes(y=MajorIncidentsScaled,fill="red"),stat="identity",alpha=0.5) +
  scale_y_continuous(name="On Time Percentage",expand=c(0,0),labels=scales::percent,
          sec.axis = sec_axis(~.*1,name="Scaled Count of Major Incidents")) +
  scale_x_date(name="Date",date_breaks = "6 months",expand=c(0,0)) + 
  scale_color_discrete(name="Time Frame",) +
  labs(title="MNR On Time Percentage and Scaled Number \nof Major Incidents by Time Frame (2020-2022)") + 
  theme_bw() +
  theme(legend.position="none",axis.text.x = element_text(angle=45,vjust=1,hjust=1),plot.title = element_text(size=12))
mnr_ts
ggsave("../../501-project-website/images/TIMESERIES-MNR-OTP.png")


### COMPARATIVE PLOTS ###

# Joining modified lirr and mnr datasets
# Add column tn enable rbind
mnr$name <- NA
# Filter to only overall time frame data for LIRR (MNR does not have more time frames)
mnr_lirr_g <- rbind(mnr,filter(lirr_g,lirr_g$name=="Overall"))
# MNR does not track OTP data prior to 2020, must filter dates of data set
mnr_lirr_g <- filter(mnr_lirr_g,mnr_lirr_g$ServiceDate>=min(mnr$ServiceDate))
# LIRR does not track OTP after October 2021, must filter dates of data set
mnr_lirr_g <- filter(mnr_lirr_g,mnr_lirr_g$ServiceDate<=max(lirr$ServiceDate))
# Comparative time series
mnr_lirr_ts <- ggplot(data=mnr_lirr_g,aes(x=ServiceDate,y=OTP,color=Agency)) +
  geom_line() +
  scale_y_continuous(name="On Time Percentage",expand=c(0,0.015),labels=scales::percent) +
  scale_x_date(name="Date",date_breaks = "3 months",expand=c(0,0)) + 
  scale_color_discrete(name="Agency") +
  labs(title="LIRR vs. MNR \nOn Time Percentage (2020-2021)") + 
  theme_bw() +
  theme(axis.text.x = element_text(angle=45,vjust=1,hjust=1))
mnr_lirr_ts
ggsave("../../501-project-website/images/TIMESERIES-MNR-LIRR-OTP.png")

# Comparative histogram of major incidents
mnr_lirr_hist <- ggplot(data=mnr_lirr_g,aes(x=ServiceDate,y=MajorIncidents,fill=Agency,color=Agency)) +
  geom_bar(stat="identity",position="dodge",alpha=0.5) +
  scale_y_continuous(name="Count of Major Incidents",expand=c(0,0),limits=c(0,25)) +
  scale_x_date(name="Date",date_breaks = "2 months",expand=c(0,0)) + 
  scale_color_discrete(name="Agency") +
  labs(title="LIRR vs. MNR \nCount of Major Incidents (2020-2021)") + 
  theme_bw() +
  theme(axis.text.x = element_text(angle=45,vjust=1,hjust=1))
mnr_lirr_hist
ggsave("../../501-project-website/images/BARCHART-MNR-LIRR-MAJINC.png")

### STATISTICAL SUMMARIES ###
print("Major Incidents Summary")
summary(mnr_lirr_g$MajorIncidents)
print("MNR OTP Sumamry")
summary(mnr$OTP)
print("LIRR OTP Summary")
summary(lirr_g$OTP)
