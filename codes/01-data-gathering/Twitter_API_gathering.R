library(tidyverse)
library(twitteR)
library(rtweet)
library(rstudioapi)

# Set working directory to raw data files for saving data later
setwd(dirname(getActiveDocumentContext()$path))
setwd("../../data/00-raw-data/")

# Read API Keys file (USE YOUR OWN IF TRYING TO RECREATE THIS)
api_keys <- read.table(r"(C:\Users\alexp\OneDrive\Documents\ANLY501\API Keys\twitter_api_keys.txt)",sep=",")
api_keys

# Defining API Keys
api_key <- api_keys[1]
api_key_secret <- api_keys[2]
api_access <- api_keys[3]
api_access_secret <- api_keys[4]
my_bearer_token <- api_keys[5]


# Authentication
setup_twitter_oauth(api_key, api_key_secret, api_access, api_access_secret)
headers <- c('Authorization' = sprintf('Bearer %s',my_bearer_token))

# Extracts past 2 weeks of NYCT Subway Tweets, used to track delays, cannot search further back than 2 weeks
#user_mta <- "@NYCTSubway"
#nyct_timeline <- userTimeline(user=user_mta,n=3200,excludeReplies = T)
#nyct_df <- twListToDF(nyct_timeline)
#write.csv(nyct_df,"NYCTSubway-Tweets-0927-1011.csv")

# Extract past 2 weeks of tweets with keywords
nyct_ops = search_tweets('("MTA" OR "NYCT") lang:en',n=3000,include_rts = F)
# Drop columns with unwritable data types
nyct_ops = nyct_ops[,-which(sapply(nyct_ops, class) == "list")]
write.csv(nyct_ops,"Opinion-Tweets-1011.csv")
