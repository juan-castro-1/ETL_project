# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:36:02 2021

@author: juan_
"""

import simfin as sf
import pandas as pd
import yfinance as yf

# Set your API-key for downloading data. This key gets the free data.
sf.set_api_key('free')


# Set the local directory where data-files are stored.
# The directory will be created if it does not already exist.
sf.set_data_dir('~/simfin_data/')

# NOMBRE EN LA BOLSA
company = 'AMZN'

# Download the data from the SimFin server and load into a Pandas DataFrame.
# annual/quarterly/ttm
BALANCE = sf.load_balance(variant='annual', market='us').loc[company, ]
CASH_FLOW = sf.load_cashflow(variant='annual', market='us').loc[company, ]
INCOME = sf.load_income(variant='annual', market='us').loc[company, ]
#PRICE = sf.load_shareprices(variant='daily', market='us').loc[company, ]
PRICE = yf.download(tickers=f'{company}',
                    period='10y',
                    interval='1mo'
                    )
PRICE.reset_index(inplace=True)
PRICE = PRICE[PRICE['Date'].dt.month == 12][['Close','Date']]


INCOME['Date'] = INCOME.index.strftime('%m-%Y')
BALANCE['Date'] = BALANCE.index.strftime('%m-%Y')
CASH_FLOW['Date'] = CASH_FLOW.index.strftime('%m-%Y')
PRICE['Date'] = PRICE['Date'].dt.strftime('%m-%Y')

PRICE = PRICE.set_index('Date')
INCOME = INCOME.set_index('Date')
BALANCE = BALANCE.set_index('Date')
CASH_FLOW = CASH_FLOW.set_index('Date')
       
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

'''
df_CF = pd.read_excel(writer, sheet_name='Cash_Flow')
df_BAL = pd.read_excel(writer, sheet_name='Balance')
df_INC = pd.read_excel(writer, sheet_name='Income')
#df_PRICE = pd.read_excel(writer, sheet_name='Price')
'''

# Profit & Loss
PL = pd.DataFrame()
PL['fiscal_year'] = CASH_FLOW['Fiscal Year']
PL['revenue'] = INCOME['Revenue']
PL['gross_profit'] = INCOME['Gross Profit']
PL['operating_income'] = INCOME['Operating Income (Loss)']
PL['EBITDA'] = INCOME['Operating Income (Loss)'] + CASH_FLOW['Depreciation & Amortization']
PL['net_profit'] = INCOME['Net Income (Common)']
PL['gross_margin'] = INCOME['Gross Profit'] / INCOME['Revenue']
PL['operating_margin'] = INCOME['Operating Income (Loss)'] / INCOME['Revenue']
PL['net_profit_margin'] = INCOME['Net Income'] / INCOME['Revenue']
PL['ROE'] = INCOME['Net Income (Common)'] / BALANCE['Total Equity']
PL['ROA'] = INCOME['Net Income (Common)'] / BALANCE['Total Assets']

'''
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
PL.index = INCOME.index
'''


# balance sheet
BSheet = pd.DataFrame()
BSheet['fiscal_year'] = CASH_FLOW['Fiscal Year']
BSheet['cash'] = BALANCE['Cash, Cash Equivalents & Short Term Investments']
BSheet['accounts_receivable'] = BALANCE['Accounts & Notes Receivable']
BSheet['total_cts_assets'] = BALANCE['Total Current Assets']
BSheet['PP&E'] = BALANCE['Property, Plant & Equipment, Net']
BSheet['total_assets'] = BALANCE['Total Assets']
BSheet['accounts_payable'] = BALANCE['Payables & Accruals']
BSheet['current_debt'] = BALANCE['Short Term Debt']
BSheet['total_cts_liabilities'] = BALANCE['Total Current Liabilities']
BSheet['long_debt'] = BALANCE['Long Term Debt']
BSheet['total_liabilities'] = BALANCE['Total Liabilities']
BSheet['total_equity'] = BALANCE['Total Equity']
'''
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
BSheet.index = BALANCE.index
'''

# cash flow
Cflows = pd.DataFrame()
Cflows['fiscal_year'] = CASH_FLOW['Fiscal Year']
Cflows['operating_cash_flow'] = CASH_FLOW['Net Cash from Operating Activities']
Cflows['investing_cash_flow'] = CASH_FLOW['Net Cash from Investing Activities']
Cflows['financing_cash_flow'] = CASH_FLOW['Net Cash from Financing Activities']
Cflows['working_capital'] = CASH_FLOW['Change in Working Capital']
Cflows['capital_expences'] = CASH_FLOW['Change in Fixed Assets & Intangibles']
Cflows['dividends'] = CASH_FLOW['Dividends Paid']
Cflows['change_cash'] = CASH_FLOW['Net Change in Cash']
Cflows['FCF'] = INCOME['Operating Income (Loss)'] + CASH_FLOW['Depreciation & Amortization' ] + CASH_FLOW['Change in Fixed Assets & Intangibles' ] + CASH_FLOW['Change in Working Capital' ] + INCOME['Income Tax (Expense) Benefit, Net']
Cflows['FCFF'] = CASH_FLOW['Net Income/Starting Line'] + CASH_FLOW['Change in Working Capital' ] + CASH_FLOW['Change in Fixed Assets & Intangibles' ]


'''
Cflows['fiscal_year'] = df_CF['Fiscal Year']
Cflows['operating_cash_flow'] = df_CF['Net Cash from Operating Activities']
Cflows['investing_cash_flow'] = df_CF['Net Cash from Investing Activities']
Cflows['financing_cash_flow'] = df_CF['Net Cash from Financing Activities']
Cflows['working_capital'] = df_CF['Change in Working Capital']
Cflows['capital_expences'] = df_CF['Change in Fixed Assets & Intangibles']
Cflows['dividends'] = df_CF['Dividends Paid']
Cflows['change_cash'] = df_CF['Net Change in Cash']
Cflows['FCF'] = df_INC['Operating Income (Loss)'] + df_CF['Depreciation & Amortization' ] + df_CF['Change in Fixed Assets & Intangibles' ] + df_CF['Change in Working Capital' ] + df_INC['Income Tax (Expense) Benefit, Net']
Cflows['FCFF'] = df_CF['Net Income/Starting Line'] + df_CF['Change in Working Capital' ] + df_CF['Change in Fixed Assets & Intangibles' ]
Cflows.index = CASH_FLOW.index
'''

# price ratios
Pratios = pd.DataFrame()
Pratios['PE'] = PRICE['Close'] 
Pratios['PE'] = Pratios['PE'].div(INCOME['Net Income (Common)'] / INCOME['Shares (Basic)'])
Pratios['PS'] = PRICE['Close']
Pratios['PS'] = Pratios['PS'].div(INCOME['Revenue'] / INCOME['Shares (Basic)'])
Pratios['Pbook'] = PRICE['Close']
Pratios['Pbook'] = Pratios['Pbook'].div(BALANCE['Total Equity'] / INCOME['Shares (Basic)'])
Pratios['PFCF'] = PRICE['Close']
Pratios['PFCF'] = Pratios['PFCF'].div(Cflows['FCF'] / INCOME['Shares (Basic)'])

# per share figures
Pshares = pd.DataFrame()
Pshares['E_per_share'] = INCOME['Net Income (Common)'] / INCOME['Shares (Basic)']
Pshares['E_per_share_d'] = INCOME['Net Income (Common)'] / INCOME['Shares (Diluted)']
Pshares['S_per_share'] = INCOME['Revenue'] / INCOME['Shares (Basic)']
Pshares['FCF_per_share'] = Cflows['FCF'] / CASH_FLOW['Shares (Basic)']
Pshares['Div_per_share'] = -CASH_FLOW['Dividends Paid'] / CASH_FLOW['Shares (Basic)']


# valuation metrics
Vmetrics = pd.DataFrame()
Vmetrics['EV/EBITDA'] = PRICE['Close'] * CASH_FLOW['Shares (Basic)']
Vmetrics['EV/EBITDA'] = Vmetrics['EV/EBITDA'] + BALANCE['Short Term Debt'] + BALANCE['Long Term Debt'] - BALANCE['Cash, Cash Equivalents & Short Term Investments'] 
op_dep = CASH_FLOW['Net Cash from Operating Activities'] + CASH_FLOW['Depreciation & Amortization']
Vmetrics['EV/EBITDA'] = Vmetrics['EV/EBITDA'] / op_dep
Vmetrics['EV/sales'] = PRICE['Close'] * CASH_FLOW['Shares (Basic)']
Vmetrics['EV/sales'] = Vmetrics['EV/sales'] + BALANCE['Short Term Debt'] + BALANCE['Long Term Debt'] - BALANCE['Cash, Cash Equivalents & Short Term Investments'] 
Vmetrics['EV/sales'] = Vmetrics['EV/sales'] / INCOME['Revenue']
Vmetrics['EV/FCF'] = PRICE['Close'] * CASH_FLOW['Shares (Basic)']
Vmetrics['EV/FCF'] = Vmetrics['EV/FCF'] + BALANCE['Short Term Debt'] + BALANCE['Long Term Debt'] - BALANCE['Cash, Cash Equivalents & Short Term Investments'] 
Vmetrics['EV/FCF'] = Vmetrics['EV/FCF'] / INCOME['Revenue']
Vmetrics['B_to_Market_value'] = BALANCE['Total Equity'] / (PRICE['Close'] * CASH_FLOW['Shares (Basic)'])


# other ratios
other = pd.DataFrame()
other['Current_ratio'] = (BALANCE['Total Current Assets'] / BALANCE['Total Current Liabilities'])
other['L_to_Eq'] = BALANCE['Total Liabilities'] / BALANCE['Total Equity']
other['debt_to_assets'] = BALANCE['Long Term Debt'] + BALANCE['Short Term Debt']
other['debt_to_assets'] = (other['debt_to_assets'] / BALANCE['Total Assets'])*100

# rates
rates = pd.DataFrame()
#rates['growth_1'] = METRICS['reinvestment_rate']*METRICS['ROE']
#rates['growth_2'] = METRICS['retention_ratio']*METRICS['ROE']
#rates['reinvestment_rate'] =  -( df_CF['Change in Working Capital' ] + df_CF['Change in Fixed Assets & Intangibles' ] ) / df_CF['Net Cash from Operating Activities']
#rates['retention_ratio'] = (df_CF['Net Income/Starting Line'] + df_CF['Dividends Paid']) / df_CF['Net Income/Starting Line']




writer_METRICS = pd.ExcelWriter(fr'{directory}\METRICS.xlsx')
PL.to_excel(writer_METRICS, sheet_name='Profit & Loss')
BSheet.to_excel(writer_METRICS, sheet_name='Balance Sheet')
Cflows.to_excel(writer_METRICS, sheet_name='Cash Flows')
Pratios.to_excel(writer_METRICS, sheet_name='P Ratios')
Pshares.to_excel(writer_METRICS, sheet_name='Share Ratios')
Vmetrics.to_excel(writer_METRICS, sheet_name='Valuation Metrics')
other.to_excel(writer_METRICS, sheet_name='Others')

writer_METRICS.save()
print('METRICS were written successfully to Excel File.')

PL.to_json(fr'{directory}\File Name.json')










