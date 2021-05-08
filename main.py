import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "your virtual twilio number"
VERIFIED_NUMBER = "your own phone number verified with Twilio"

#company to get alerts on
STOCK_NAME = "ENTER STOCK TICKER"
COMPANY_NAME = "COMPANY NAME"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "YOUR OWN API KEY FROM ALPHAVANTAGE"
NEWS_API_KEY = "YOUR OWN API KEY FROM NEWSAPI"
TWILIO_SID = "YOUR TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#header parameters
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
#Get yesterday's closing stock price
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yday_data = data_list[0]
yday_closing_price = yday_data["4. close"]
# print(yesterday_closing_price)

#Get the day before yesterday's closing stock price
day_before_yday_data = data_list[1]
day_before_yday_closing_price = day_before_yday_data["4. close"]
# print(day_before_yesterday_closing_price)

#Find the difference between the last two days
difference = float(yday_closing_price) - float(day_before_yday_closing_price)
movement = None
if difference > 0:
    movement = "🔺"
else:
    movement = "🔻"

#Percent difference in price between the previous two days.
diff_percent = round((difference / float(yday_closing_price)) * 100)
# print(diff_percent)


#If percent difference is greater than 5 then get the first three news articles, then send each article to
# the number provided
if abs(diff_percent) > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    #Pull the first 3 articles.
    three_articles = articles[:3]
    # print(three_articles)

    #Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {movement}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    # print(formatted_articles)

    #Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )

