#Harmonizing Data
#Scripts for harmonizing project data – goal is to create a large data set with the same columns across all cities

#import libraries
import pandas as pd
import numpy as np
import geopandas as geo
from dateutil import parser

#import data
pittsburgh = pd.read_csv('Resources/AlleghenyCountyRealEstateSales.csv')
connecticut = pd.read_csv('Resources/CTRealEstateSales.csv')
detroit = pd.read_csv('Resources/DetroitRealEstateSales.csv')
philly = pd.read_csv('Resources/PhillyRealEstateSales.csv')
chicago = pd.read_csv('Resources/ChicagoRealEstateSales.csv')

#filter philly data to just deed transfers
philly = philly.dropna(subset = ['total_consideration'])
philly = philly[philly['display_date'] > '2000-01-01']

#fix date formats in CT, Detroit, and Chicago

def standardize_date(date_str):
    try:
        if isinstance(date_str, float) or date_str is None:
            return None  # Handle NaN or None values gracefully
        parsed_date = parser.parse(str(date_str))  # Convert to string before parsing
        return parsed_date.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return None  # Return None if the date cannot be parsed
    
chicago['sale_date'] = chicago['sale_date'].apply(standardize_date)
connecticut['Date Recorded'] = connecticut['Date Recorded'].apply(standardize_date)
detroit['Sale Date'] = detroit['Sale Date'].apply(standardize_date)

print(len(philly))
print(philly.head())

#final dataset columns: address, location (lat/lon), sale date, sale price
final = pd.DataFrame({
    'city': [], 
    'address': [],
    'zip_code': [],
    'parcel_id': [],
    'location': [],
    'sale_date': [],
    'sale_price': []
})


#function to generalize locating columns
#input: dataframe, list of target columns in order of final cols
#output: returns clean df with target columns
def find_cols(df, col_list):
    clean_df = pd.DataFrame()
    final_cols = ['city', 'address', 'zip_code',
                  'parcel_id', 'location', 'sale_date', 'sale_price']
    

    for i in range(len(col_list)):
        if pd.isna(col_list[i]):
            clean_df[final_cols[i]] = [np.nan]*len(df)
        else:
            clean_df[final_cols[i]] = df[col_list[i]]

    return clean_df

#pittsburgh
df = pittsburgh
col_list = ['PROPERTYCITY', 'FULL_ADDRESS', 'PROPERTYZIP', 'PARID',
             np.nan, 'SALEDATE', 'PRICE']
clean_pitt = find_cols(df, col_list)

print(len(final))

#connecticut
df = connecticut
col_list = ['Town', 'Address', np.nan, 'Serial Number', 'Location', 
            'Date Recorded', 'Sale Amount']

clean_ct = find_cols(df, col_list)

#detroit
df = detroit
detroit['Location'] = geo.points_from_xy(detroit['x'], detroit['y'])
col_list = [np.nan, 'Street Address', np.nan, 'Parcel Number', 
            'Location', 'Sale Date', 'Sale Price']

clean_detroit = find_cols(df, col_list)
clean_detroit['city'] = 'DETROIT'

#philly
df = philly
col_list = [np.nan, 'street_address', 'zip_code', 'document_id', 
            np.nan, 'recording_date', 'total_consideration']

clean_philly = find_cols(df, col_list)
clean_philly['city'] = 'PHILADELPHIA'

#chi-town
df = chicago
col_list = [np.nan, np.nan, 'pin', np.nan, 'sale_date', 'sale_price']
clean_chicago = find_cols(df, col_list)
clean_chicago['city'] = 'CHICAGO'

#concat all clean dfs
final = pd.concat([clean_chicago, clean_philly, clean_detroit, clean_pitt, clean_ct])

print(len(final))
print(final.head())

final.to_csv("Resources/all_cities.csv")