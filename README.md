# Final Project
Financial Data Analysis

## Data
### Ticker List
![Data](assets/ticker_data.PNG)

### Tools (Select box, Text box, Search button)
![Tools](assets/tools_for_user_input.PNG)

### Stock Data
![Data](assets/apple_stock_data.PNG)

## Transformation
For Collect the data, we used a Polygon API and we got data in json format and then we convert those data into pandas dataframe.
After get the data in dataframe, we worked on clean the data like change the format of date.
Then we display our data in our streamlit application.

First we bind the list of Tickers and after that we add one dropdown list for names of stock and also one textbox if anyone doen't find their stock name in the dropdown list and then we add a submit button for review that selected stock data.

After press the search button, you can see the data of your stock and some visualizations for analysis.

## Visualizations

### Line chart for stock open price per month and year
![Data](assets/line_chart_for_open.PNG)

### Line chart for stock close price per month and year
![Data](assets/line_chart_for_close.PNG)

### Multiple Line chart for stock high and low price per month and year
![Data](assets/line_chart_for_high&low.PNG)

### Bar chart for Number of Transaction per month and year
![Data](assets/bar_chart_for_volume.PNG)

### Pie chart for volume percentage per year
![Data](assets/pie_chart_for_volume.PNG)

## App
In our Application, we have done an analysis for Financial Data and for that we add some visualizations so people can see the trends and it helps them for buy or sell the stocks.
