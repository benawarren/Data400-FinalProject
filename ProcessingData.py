#import libraries
import pandas as pd

#import data for all cities
df = pd.read_csv('Resources/all_cities.csv')

#filter to useable data
# - Has address or location data
# - Has sale price and sale date
# - sale price greater than 10K (smaller values likely for friends and family transfers)

#address or location data
filtered = df[(df['location'].notna() & df['location'].str.strip().ne('')) | 
                 (df['address'].notna() & df['address'].str.strip().ne(''))]

#sale price and sale date
filtered = filtered.dropna(subset=['sale_price', 'sale_date'])

#sale price > 10K
filtered = filtered[filtered['sale_price'] > 10000]

filtered.to_csv('Resources/filtered.csv')