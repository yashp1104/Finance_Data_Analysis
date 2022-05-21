import streamlit as st
from logging import getLogger
import numpy as np
import pandas as pd
import datetime as dt
import requests
import json
<<<<<<< HEAD
=======

>>>>>>> 6c0e298931bbac9ce455e30cd29fe070795109b6

# Sceen size
st.set_page_config(layout="wide")

# Create Logger
loggers =  getLogger()

#Start of API Credentials
ALPACA_API_KEY = 'tpHEpdlolUR703YTAdrvOHaUMW6PEDPw' #os.environ.get('ALPACA_API_KEY')
# URL for all the tickers on Polygon
# POLYGON_TICKERS_URL = 'https://api.polygon.io/v2/reference/tickers?page={}&apiKey={}'
POLYGON_TICKERS_URL = 'https://api.polygon.io/v3/reference/tickers?active={}&sort=ticker&order={}&limit={}'
# URL FOR PRICING DATA - Note, getting pricing that is UNADJUSTED for splits, I will try and adjust those manually
POLYGON_AGGS_URL = 'https://api.polygon.io/v2/aggs/ticker/{}/range/{}/{}/{}/{}'
# URL FOR DIVIDEND DATA
POLYGON_DIV_URL = 'https://api.polygon.io/v2/reference/dividends/{}?apiKey={}'
# URL FOR STOCK SPLITS
POLYGON_SPLIT_URL = 'https://api.polygon.io/v2/reference/splits/{}?apiKey={}'
#URL FOR TICKER TYPES
POLYGON_TYPES_URL = 'https://api.polygon.io/v2/reference/types?apiKey={}'
#End of API Credentials

#Start of Polygon API Code
class polygon_api:
    '''Authorization: Bearer tpHEpdlolUR703YTAdrvOHaUMW6PEDPw
    'https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2020-06-01/2020-06-17?apiKey=tpHEpdlolUR703YTAdrvOHaUMW6PEDPw'
    demo url = 'https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2021-07-22/2021-07-22?adjusted=true&sort=asc&limit=120&apiKey=tpHEpdlolUR703YTAdrvOHaUMW6PEDPw
    token is unique token for authorization 
    url is base url of the the api'''

    def __init__(self) :
        self.token = 'tpHEpdlolUR703YTAdrvOHaUMW6PEDPw'
        self.authorization = {'Authorization':'Bearer '+ self.token}
        # self.url = 'https://api.polygon.io/v2/'

    def get_tickers(self,active=True,order='asc',limit=1000):
        '''this method is use to get list of tickers
        return : 
        list of tickers '''
        try:
            loggers.error(f'get ticker : Try block called')

            ticker_url = POLYGON_TICKERS_URL.format(active,order,limit)
            ticker_json = self.get_data(ticker_url)
            # print(ticker_json)
            ticker_df = pd.DataFrame(ticker_json['results'])
            # ticker_df.to_csv('data/tickers/tickerlist.csv', index=False)
            return ticker_df
        except Exception as e:
            loggers.error(f'get ticker : exception block called {e}')


    def get_aggregate(self,stocksTicker,multiplier,timespan,from_date,to_date):
        ''' Request : 
            Stock Ticker : str :  Name of Stock
            Multiplier : int : Count of timespan
            timespan : string :day / hours / minute  
            Multiplier is 5 and timespan is minute then 5-minute bar will return.
            from_date : datetime as str : from date 
            to_date : datetime as str : to date 
            Method: get
            request url : /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} 
            Response : Data Frame of the particular stock '''    
        try:
            loggers.info('Start get_aggregate : try block method')
            method_url = (POLYGON_AGGS_URL.format(stocksTicker,multiplier,timespan,from_date,to_date)) # f'aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from_date}/{to_date}'
            
            loggers.info('Get method call: try block method')
            response_json = self.get_data(method_url)
            loggers.info(f'Get method called: try block method \n {response_json}')
            # aggreget_response_df = pd.DataFrame(response_json)
            if response_json['status']  != 'ERROR':
                if response_json['queryCount'] > 0:
                    loggers.info('get_aggregate : If block Call')
                    # print(response_json)
                    stock_name = response_json['ticker']
                    stock_result = response_json['results']

                    aggreget_response_df = pd.DataFrame(stock_result)
                    aggreget_response_df = aggreget_response_df.rename({'v':'volume','vw':'volume_weight','o':'open','c':'close','h':'high','l':'low','t':'date','n':'no_of_trans'}, axis=1)  # new method
                    # loggers.info(f'convert to df :   {aggreget_response_df}')
                    # aggreget_response_df['t'] = pd.to_datetime(aggreget_response_df['t'], format='%Y%m%d')
                    aggreget_response_df.date = aggreget_response_df["date"].apply(self.get_date)

                    aggreget_response_df.sort_values(by=['date'], inplace=True)
                    stock_details = (stock_name,aggreget_response_df)
                    # aggreget_response_df.to_csv(f'data/stockdetails/{stock_name}.csv')
                    return stock_details
                else:
                    loggers.info('get_aggregate : Else block Call')
                    stock_details = (f'No Data Found For  {stocksTicker}',[])
                    return stock_details
            else:
                stock_details = (f'Maximum limit of API Call is Reached.',[])
                return stock_details
        except Exception as e:
            loggers.error(f'get_aggregate : Except block Call {e}')

    def get_data(self,method_url):
        '''THIS METHOD IS USE FOR THE CALL THE GET API TO polygon.io 
        Request :
        method url: url of the method with get request  
        Response : 
        json text 
        ticker : stock name
        result : stock detail
            'o' : The open price for the symbol in the given time period
            'c' : The highest price for the symbol in the given time period.
            'h' : The highest price for the symbol in the given time period.
            'l' : The open price for the symbol in the given time period
            'v' : The trading volume of the symbol in the given time period.
            'vw' : The volume weighted average price
            't' : The Unix Msec timestamp for the start of the aggregate window.
            'n' : The open price for the symbol in the given time period '''
        try:
            loggers.info('get_data : try block')
            # api_url = self.url + method_url

            loggers.info(f' get request url : {method_url}')
            response = requests.get(method_url,  headers=self.authorization)
            agg_content = json.loads(response.text)
            return agg_content
        except Exception as e:
            loggers.error(f'get_data : except Block {e}')
            raise e
    
    def get_date(self, created):
        '''this method is convert timestamp to data time formate''' 
        try:
            # loggers.info(f'get_date : try block call {created}')
            return dt.datetime.fromtimestamp((created/1000)).strftime('%Y-%m')
        except Exception as e:
            loggers.info(f'get_date : exception block call { e} ')
#End of Polygon API Code


def stock_details_fun(stock_details):
    # display the details of stock 
    st.subheader(f'{stock_details[0]} Stock Data')
    st.write(stock_details[1])

    if stock_details[0].upper() == "APPL":
        # line chart for open
        st.subheader(f'{stock_details[0]} Open stock price data')
        df = pd.DataFrame({
        'date': stock_details[1]['date'],
        'open stock_price': stock_details[1]['open']
        })
        df = df.rename(columns={'date':'index'}).set_index('index')
        st.line_chart(df)
    else :
        loggers.info("test")
        stock_details_AAPL_from_csv = pd.read_csv("data/stockdetails/AAPL.csv")
        # loggers.info(stock_details_from_csv)
        # stock_details = pd.DataFrame(stock_details_from_csv)

        stock_details_def = ('APPL',stock_details_AAPL_from_csv)
        # Multiple Line chart for high and low stock_price
        st.subheader(f'{stock_details[0]} Comapare stock price data')
        compare_stock = pd.DataFrame({
        'date': stock_details[1]['date'],
        'APPL Open stock_price': stock_details_def[1]['open'],
        'Open stock_price': stock_details[1]['open']
        })
        loggers.info(compare_stock)
        compare_stock = compare_stock.rename(columns={'date':'index'}).set_index('index')
        # chart_data = compare_stock
        st.line_chart(compare_stock)


    # line chart for open
    st.subheader(f'{stock_details[0]} Open stock price data')
    df = pd.DataFrame({
    'date': stock_details[1]['date'],
    'open stock_price': stock_details[1]['open']
    })
    df = df.rename(columns={'date':'index'}).set_index('index')
    st.line_chart(df)

    # line chart for close
    st.subheader(f'{stock_details[0]} Close stock price data')
    df = pd.DataFrame({
    'date': stock_details[1]['date'],
    'close stock_price': stock_details[1]['close']
    })
    df = df.rename(columns={'date':'index'}).set_index('index')
    st.line_chart(df)

    # Multiple Line chart for high and low stock_price
    st.subheader(f'{stock_details[0]} High and Low stock price data')
    df = pd.DataFrame({
    'date': stock_details[1]['date'],
    'low stock_price': stock_details[1]['low'],
    'high stock_price': stock_details[1]['high']
    })
    df = df.rename(columns={'date':'index'}).set_index('index')
    chart_data = df
    st.line_chart(chart_data)
    
    #Bar Chart
    st.header(f"No of transactions by month")
    df = pd.DataFrame({
    'date': stock_details[1]['date'],
    'num of transactions': stock_details[1]['no_of_trans']
    })
    df = df.rename(columns={'date':'index'}).set_index('index')
    chart_data = df
    st.bar_chart(chart_data)

title_col1,title_col2,title_col3 = st.columns([3,4,2])
with title_col1:
    pass
with title_col2:
    st.markdown("""# *Finance Data Analysis*""")
with title_col3:
    pass

#Start of Ticker list defult data  
aggreget_api = polygon_api()

# Get List of Ticker
# ticker_list = aggreget_api.get_tickers()  #drirect api call for get ticker list
ticker_list = pd.read_csv("data/tickers/tickerlist.csv")
#Get useable data from csv
updated_ticker_list = ticker_list.iloc[:, 0:8]
# Display List of Ticker
st.subheader(f'Ticker List')
st.write(updated_ticker_list)



# get list of ticker and name
ticker_dd = ticker_list[['name','ticker']]
# Combain Name and ticker
combine_ticker_name = ticker_dd['ticker'].str.cat(ticker_dd[['name']], sep='-')
# get the index of AAPL ticker or default load
default_ix = combine_ticker_name.tolist().index('AAPL-Apple Inc.')
stock_details = []
todays_date = dt.datetime.now().date() 

#Start of search
def getTickerdetails(ticker_name,from_date,to_date):
    if(ticker_name):
        loggers.info('getTickerdetails : if Condition BEFOR SPLIT called tikker Name {}'.format(ticker_name))
        ticker_value = ticker_name.split('-')
        ticker_name = ticker_value[0]

        loggers.info('getTickerdetails : if Condition called tikker Name {}'.format(ticker_name))
        stock_details = aggreget_api.get_aggregate(ticker_name.upper(),1,'month',from_date,to_date)

        if len(stock_details[1]) > 0:
            stock_details_fun(stock_details)

        else:
            st.warning(f' {stock_details[0]}')
    else:
        loggers.info('getTickerdetails : else Condition called tikker Name {}'.format(ticker_name))
        st.warning('Please Enter Tickker Name')
#End of search

# from_date = st.sidebar.date_input('From Date')
# to_date = st.sidebar.date_input('To Date', max_value =todays_date)
# to_date = st.sidebar.multiselect('TickerList',combine_ticker_name)



#start of select box,text box, and search button design
col1,col2,col3 = st.columns([1,1,1])
with col1:
    # Create Select box
    ticker_name = st.selectbox('Select Ticker :',combine_ticker_name,index = default_ix)
with col2:
    ticker_txt_Name = st.text_input('Enter Ticker:',key='txt_ticker_name')
# with col3:
    # multiselect_ticker = st.multiselect('Multi Select Ticker ',combine_ticker_name)
date_col1,date_col2,date_col3 = st.columns([1,1,1])

with date_col1:
    from_date = st.date_input('From Date')
    
with date_col2:
    to_date = st.date_input('To Date', max_value =todays_date)
loggers.info(from_date)
loggers.info(to_date)

if ticker_txt_Name:
    ticker_name = ticker_txt_Name
if st.button('Search'):
    getTickerdetails(ticker_name,from_date,to_date)
    default_load = False
else:
    stock_details_from_csv = pd.read_csv("data/stockdetails/AAPL.csv")
    # loggers.info(stock_details_from_csv)
    # stock_details = pd.DataFrame(stock_details_from_csv)

    stock_details_def = ('APPL',stock_details_from_csv)
    loggers.info(stock_details_def)
    stock_details_fun(stock_details_def)
    #end of select box,text box, and search button design

    
