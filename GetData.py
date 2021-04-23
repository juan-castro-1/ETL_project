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
company = 'MELI'

# Download the data from the SimFin server and load into a Pandas DataFrame.
# annual/quarterly/ttm
BALANCE = sf.load_balance(variant='annual', market='us').loc[company, ]
CASH_FLOW = sf.load_cashflow(variant='annual', market='us').loc[company, ]
INCOME = sf.load_income(variant='annual', market='us').loc[company, ]

directory = fr"C:\Users\juan_\Dropbox\Mi PC (LAPTOP-H9MAOJRB)\Desktop\Valuation\US_Stocks\Data\{company}"

writer = pd.ExcelWriter(fr'{directory}\DATA.xls')

# write dataframe to excel
BALANCE.to_excel(writer, sheet_name='Balance')
CASH_FLOW.to_excel(writer, sheet_name='Cash_Flow')
INCOME.to_excel(writer, sheet_name='Income')
# save the excel
writer.save()
print('DATA was written successfully to Excel File.')


import pandas as pd

df_CF = pd.read_excel(writer, sheet_name='Cash_Flow')
df_BAL = pd.read_excel(writer, sheet_name='Balance')
df_INC = pd.read_excel(writer, sheet_name='Income')

METRICS = pd.DataFrame()
METRICS['fiscal_year'] = df_CF['Fiscal Year']
METRICS['FCF'] = df_INC['Operating Income (Loss)'] + df_CF['Depreciation & Amortization' ] + df_CF['Change in Fixed Assets & Intangibles' ] + df_CF['Change in Working Capital' ] + df_INC['Income Tax (Expense) Benefit, Net']
METRICS['FCFF'] = df_CF['Net Income/Starting Line'] + df_CF['Change in Working Capital' ] + df_CF['Change in Fixed Assets & Intangibles' ]
METRICS['reinvestment_rate'] =  -( df_CF['Change in Working Capital' ] + df_CF['Change in Fixed Assets & Intangibles' ] ) / df_CF['Net Cash from Operating Activities']
METRICS['ROE'] = df_INC['Net Income (Common)'] / df_BAL['Total Equity']
METRICS['retention_ratio'] = (df_CF['Net Income/Starting Line'] + df_CF['Dividends Paid']) / df_CF['Net Income/Starting Line']
METRICS['growth_1'] = METRICS['reinvestment_rate']*METRICS['ROE']
METRICS['growth_2'] = METRICS['retention_ratio']*METRICS['ROE']



writer_METRICS = pd.ExcelWriter(fr'{directory}\METRICS.xls')
METRICS.to_excel(writer_METRICS)
writer_METRICS.save()
print('METRICS were written successfully to Excel File.')

















