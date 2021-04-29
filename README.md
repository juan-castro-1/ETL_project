# ETL stocks project

## Data
Data comes from SimFin awesome API: https://simfin.com/

```bash
pip install simfin
```
## Getting Data
The GetData.py file lets you download the fundamentals data, Income Statement, Balance & Cash Flow. 
Choose a public company and create a folder with the same name* and modified the .py file where:

*use the company trading name not the original name, ig: AAPL insted of APPLE

```
company = 'NAME OF COMPANY'
```
### Other .. work in progress
Also, by running GetData.py it will create a METRICS.xls in the folder you created before. 
In this you will find usefull metrics such as Free Cash Flows (FCF) and more ... currently being developed

# In the future
I'll add more data from the US Stock market...

Sync data to a data visualization plataform for better analysis...

Use some cloud database to store data (AWS, Azure, etc ..)

And more

