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
PRICE = sf.load_shareprices(variant='daily', market='us').loc[company, ]

directory = fr"C:\Users\juan_\Dropbox\Mi PC (LAPTOP-H9MAOJRB)\Desktop\Valuation\US_Stocks\Data\{company}"

writer = pd.ExcelWriter(fr'{directory}\DATA.xls')

# write dataframe to excel
BALANCE.to_excel(writer, sheet_name='Balance')
CASH_FLOW.to_excel(writer, sheet_name='Cash_Flow')
INCOME.to_excel(writer, sheet_name='Income')
PRICE.to_excel(writer, sheet_name='Price')
# save the excel
writer.save()
print('DATA was written successfully to Excel File.')


df_CF = pd.read_excel(writer, sheet_name='Cash_Flow')
df_BAL = pd.read_excel(writer, sheet_name='Balance')
df_INC = pd.read_excel(writer, sheet_name='Income')
#df_PRICE = pd.read_excel(writer, sheet_name='Price')


# Profit & Loss
PL = pd.DataFrame()
PL['fiscal_year'] = df_CF['Fiscal Year']
PL['revenue'] = df_INC['Revenue']
PL['gross_profit'] = df_INC['Gross Profit']
PL['operating_income'] = df_INC['Operating Income (Loss)']
PL['EBITDA'] = df_INC['Operating Income (Loss)'] + df_CF['Depreciation & Amortization']
PL['net_profit'] = df_INC['Net Income (Common)']
PL['gross_margin'] = df_INC['Gross Profit'] / df_INC['Revenue']
PL['operating_margin'] = df_INC['Operating Income (Loss)'] / df_INC['Revenue']
PL['net_profit_margin'] = df_INC['Net Income'] / df_INC['Revenue']
PL['ROE'] = df_INC['Net Income (Common)'] / df_BAL['Total Equity']
PL['ROA'] = df_INC['Net Income (Common)'] / df_BAL['Total Assets']



# balance sheet
BSheet = pd.DataFrame()
BSheet['fiscal_year'] = df_CF['Fiscal Year']
BSheet['cash'] = df_BAL['Cash, Cash Equivalents & Short Term Investments']
BSheet['accounts_receivable'] = df_BAL['Accounts & Notes Receivable']
BSheet['total_cts_assets'] = df_BAL['Total Current Assets']
BSheet['PP&E'] = df_BAL['Property, Plant & Equipment, Net']
BSheet['total_assets'] = df_BAL['Total Assets']
BSheet['accounts_payable'] = df_BAL['Payables & Accruals']
BSheet['current_debt'] = df_BAL['Short Term Debt']
BSheet['total_cts_liabilities'] = df_BAL['Total Current Liabilities']
BSheet['long_debt'] = df_BAL['Long Term Debt']
BSheet['total_liabilities'] = df_BAL['Total Liabilities']
BSheet['total_equity'] = df_BAL['Total Equity']


# cash flow
Cflows = pd.DataFrame()
Cflows['fiscal_year'] = df_CF['Fiscal Year']
Cflows['operating_cash_flow'] = df_CF['Net Cash from Operating Activities']
Cflows['investing_cash_flow'] = df_CF['Net Cash from Investing Activities']
Cflows['financing_cash_flow'] = df_CF['Net Cash from Financing Activities']
Cflows['working_capital'] = df_CF['Change in Working Capital']
Cflows['PP&E'] = df_CF['Change in Fixed Assets & Intangibles']
Cflows['dividends'] = df_CF['Dividends Paid']
Cflows['change_cash'] = df_CF['Net Change in Cash']
Cflows['FCF'] = df_INC['Operating Income (Loss)'] + df_CF['Depreciation & Amortization' ] + df_CF['Change in Fixed Assets & Intangibles' ] + df_CF['Change in Working Capital' ] + df_INC['Income Tax (Expense) Benefit, Net']
Cflows['FCFF'] = df_CF['Net Income/Starting Line'] + df_CF['Change in Working Capital' ] + df_CF['Change in Fixed Assets & Intangibles' ]


# profit ratios


# growth rate
#METRICS = pd.DataFrame()
#METRICS['growth_1'] = METRICS['reinvestment_rate']*METRICS['ROE']
#METRICS['growth_2'] = METRICS['retention_ratio']*METRICS['ROE']
#METRICS['reinvestment_rate'] =  -( df_CF['Change in Working Capital' ] + df_CF['Change in Fixed Assets & Intangibles' ] ) / df_CF['Net Cash from Operating Activities']
#METRICS['retention_ratio'] = (df_CF['Net Income/Starting Line'] + df_CF['Dividends Paid']) / df_CF['Net Income/Starting Line']


#writer_METRICS = pd.ExcelWriter(fr'{directory}\METRICS.xls')
#PL.to_excel(writer_METRICS, sheet_name='Profit & Loss')
#BSheet.to_excel(writer_METRICS, sheet_name='Balance Sheet')
#Cflows.to_excel(writer_METRICS, sheet_name='Cash Flows')
#writer_METRICS.save()
#print('METRICS were written successfully to Excel File.')




writer_json = fr'{directory}\PL.json'
PL.to_json(writer_json, orient='records')

print('METRICS were written successfully to Json File.')



'''
HACER UN JSON POR CADA METRICS
'''











