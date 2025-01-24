import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

def get_company_info(comapny_name):
    try:
       company_ticker = yf.Ticker(company_name)
       company_info = company_ticker.info
       if company_info:
          return company_info
       else:
           return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_stock_historical_data(company_name, start_date, end_date):
    try:
        company_ticker = yf.Ticker(company_name)
        historical_data = company_ticker.history(start=start_date, end=end_date)
        historical_data['MA50'] = historical_data['Close'].rolling(window=50).mean()
        historical_data['MA200'] = historical_data['Close'].rolling(window=200).mean()
        return historical_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def predict_high_price(historical_data, future_date):
    # try:
    #     future_date = datetime.strptime(future_date_str, '%Y-%m-%d').date()
    # except ValueError:
    #     return "Invalid date format. Please use YYYY-MM-DD."

    last_available_date = historical_data.index[-1].date()

    if future_date <= last_available_date:
      return f"Prediction not possible.  The requested date is in the past or present.  Last date in data: {last_available_date}"

    # Simple prediction based on the trend of the moving averages:
    if historical_data['MA50'][-1] > historical_data['MA200'][-1]:
        prediction = "Upward trend"
        # Estimate a potential increase (this is a very basic example)
        potential_increase = (historical_data['High'][-1] - historical_data['Low'][-1]) * 0.10 # 10% of the daily range
        predicted_high = historical_data['High'][-1] + potential_increase
    else:
        prediction = "Downward or sideways trend"
        # Estimate a potential decrease
        potential_decrease = (historical_data['High'][-1] - historical_data['Low'][-1]) * 0.05 # 5% of the daily range
        predicted_high = historical_data['High'][-1] - potential_decrease


    return f"Predicted high price for {future_date}: {predicted_high:.2f}, Trend: {prediction}. Disclaimer: This is a very basic prediction model."


if __name__ == "__main__":
    st.title("company stock khundli")
    company_name = st.text_input("Enter company name:")
    print(company_name)
    st.write("This is a simple web app to get the stock price of a company.")
    if st.button("Get Stock details"):
        company_info=get_company_info(company_name)
        st.write(f"Company Name: {company_info.get('longName', company_name)}")
        st.write(f"Company Sector: {company_info.get('sector', 'Not Available')}")
        st.write(f"Company Industry: {company_info.get('industry', 'Not Available')}")
        st.write(f"Company Country: {company_info.get('country', 'Not Available')}")
        st.write(f"Company Open: {company_info.get('open', 'Not Available')}")
        st.write(f"Company Phone: {company_info.get('phone', 'Not Available')}")
        st.write(f"Company Website: {company_info.get('website', 'Not Available')}")
        st.write(f"Company Day_Low: {company_info.get('dayLow', 'Not Available')}")
        st.write(f"Company Day_High: {company_info.get('dayHigh', 'Not Available')}")
    start_date = st.date_input("Enter start date")
    st.write(f"your starting date is : {start_date}")
    end_date = st.date_input("Enter end date")
    st.write(end_date)
    future_date = st.date_input("Enter the date of prediction")
    st.write(future_date)
    if st.button("get stock future prediction"):
        historical_data = get_stock_historical_data(company_name, start_date, end_date)
        print(historical_data)
        if historical_data is not None:
            result=predict_high_price(historical_data,future_date)
            st.write(result)

        
