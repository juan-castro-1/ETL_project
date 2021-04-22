# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:36:02 2021

@author: juan_
"""

import simfin as sf
import pandas as pd

# Set your API-key for downloading data. This key gets the free data.
sf.set_api_key('free')


# Set the local directory where data-files are stored.
# The directory will be created if it does not already exist.
sf.set_data_dir('~/simfin_data/')

# NOMBRE EN LA BOLSA
company = 'AAPL'

# Download the data from the SimFin server and load into a Pandas DataFrame.
# annual/quarterly/ttm
BALANCE = sf.load_balance(variant='annual', market='us').loc[company, ]
CASH_FLOW = sf.load_cashflow(variant='annual', market='us').loc[company, ]
INCOME = sf.load_income(variant='annual', market='us').loc[company, ]

# Print the first rows of the data.
#print(CASH_FLOW.columns)
#MMM = df.loc['MMM', ]
#MMM = pd.DataFrame(MMM)
#del df

#directory = 'C:\Users\juan_\Dropbox\Mi PC (LAPTOP-H9MAOJRB)\Desktop\Valuation\US_Stocks\Data\{company}'


# create excel writer object
writer = pd.ExcelWriter(r'C:\Users\juan_\Dropbox\Mi PC (LAPTOP-H9MAOJRB)\Desktop\Valuation\US_Stocks\Data\APPLE\DATA.xls')

#writer = pd.ExcelWriter(r'directory\DATA.xls')

# write dataframe to excel
BALANCE.to_excel(writer, sheet_name='Balance')
CASH_FLOW.to_excel(writer, sheet_name='Cash_Flow')
INCOME.to_excel(writer, sheet_name='Income')
# save the excel
writer.save()
print('DataFrame is written successfully to Excel File.')
