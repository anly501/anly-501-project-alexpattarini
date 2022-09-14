
import numpy as np
import pandas as pd
from sodapy import Socrata

# Importing API Keys
with open(R"C:\Users\alexp\OneDrive\Documents\ANLY501\API Keys\mta_keys.txt") as f:
    mta_api = f.read()
mta_api = mta_api.split(",")

# Parse API Keys from local machine
api_key = mta_api[0]
api_secret = mta_api[1]
app_token = mta_api[2]
app_token_secret = mta_api[3]
username = mta_api[4]
pwd = mta_api[5]

# Access MTA Socrata API
client = Socrata("data.ny.gov",app_token,username=api_key,password=api_secret)

# GET fare card history data and move to data frame --- 98988 cuts off the data set at 2017 and beyond
results = client.get("v7qc-gwpn",limit=98988)
#print(results)
fare_card_df = pd.DataFrame(results)
#print(fare_card_df.head())
# Export df to csv for later use
fare_card_df.to_csv(R"./data/00-raw-data/MTA-Fare-Card-Data-From-2010.csv")

# GET Customer Feedback metrics
results = client.get("hrau-ksig")
#print(results.head())
feedback_df = pd.DataFrame(results)
#print(feedback_df.head())
# Export df to csv for later use
feedback_df.to_csv(R"./data/00-raw-data/MTA-Customer-Feedback.csv")

# GET Geospatial data regarding subway stations
results = client.get("i9wp-a4ja",limit=1900)
station_loc_df = pd.DataFrame(results)
station_loc_df.to_csv(R"./data/00-raw-data/MTA-Subway-Station-Location-Data.csv")