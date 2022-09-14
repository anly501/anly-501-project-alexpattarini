
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
# GET fare card history data and move to data frame
results = client.get("v7qc-gwpn")
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

# GET System Usage 2021
results = client.get("uu7b-3kff")
system_usage_df = pd.DataFrame(results)
system_usage_df.to_csv(R"./data/00-raw-data/MTA-System-Usage-2021.csv")

# GET System Usage 2020
results = client.get("py8k-a8wg")
system_usage_df = pd.DataFrame(results)
system_usage_df.to_csv(R"./data/00-raw-data/MTA-System-Usage-2020.csv")

# GET System Usage 2019
results = client.get("xfn5-qji9")
system_usage_df = pd.DataFrame(results)
system_usage_df.to_csv(R"./data/00-raw-data/MTA-System-Usage-2019.csv")

# GET System Usage 2018
results = client.get("bjcb-yee3")
system_usage_df = pd.DataFrame(results)
system_usage_df.to_csv(R"./data/00-raw-data/MTA-System-Usage-2018.csv")

# GET System Usage 2017
results = client.get("v5y5-mwpb")
system_usage_df = pd.DataFrame(results)
system_usage_df.to_csv(R"./data/00-raw-data/MTA-System-Usage-2017.csv")