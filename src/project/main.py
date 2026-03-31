import eurostat
import pandas as pd

DATASET = "prc_hpi_a"

# House pricing index from 2005-2024 across all european coutries
print(f"Fetching '{DATASET}' from Eurostat …")
raw = eurostat.get_data_df(DATASET)
# normalizing dataframe
raw = raw.drop(columns=['freq', 'unit'])
raw = raw.rename(columns={'geo\\TIME_PERIOD': 'geo'})
#printing df information
print(f"Raw shape: {raw.shape}")
print(raw)

'''
dataframe explenation:
DW_EXST = Existing dwellings (second-hand)
DW_NEW = New dwellings (there will be other rows with this)
DW_TOT = Total (both combined)

everything else I bleieve is self explanatory, better explenation will be added in further versions
'''

#plot idea 1, HPI in Spain compared to the avg HPI in europe across time 

