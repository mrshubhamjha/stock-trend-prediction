import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

start = '2010-01-01'
end = '2019-12-31'

st.title('Stock Trend Prediction')

user_input = st.text_input('Enter Stock Ticker', 'AAPL')
df = yf.download(user_input, start=start, end=end)

# Describing data
st.subheader('Data from 2010 - 2019')
st.write(df.describe())

# Plotting closing price
st.subheader('Closing Price vs Time Chart')
fig = plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Close'])
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title(f'{user_input} Closing Price')
st.pyplot(fig)

# Calculating and plotting 100-day moving average
df['100MA'] = df['Close'].rolling(window=100).mean()
st.subheader('Closing Price vs Time Chart with 100MA')
fig = plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Close'], label='Close Price')
plt.plot(df.index, df['100MA'], label='100-Day Moving Average', color='orange')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title(f'{user_input} Closing Price and 100-Day Moving Average')
plt.legend()
st.pyplot(fig)

# Calculating and plotting 200-day moving average
df['200MA'] = df['Close'].rolling(window=200).mean()
st.subheader('Closing Price vs Time Chart with 200MA')
fig = plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Close'], label='Close Price')
plt.plot(df.index, df['200MA'], label='200-Day Moving Average', color='red')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title(f'{user_input} Closing Price and 200-Day Moving Average')
plt.legend()
st.pyplot(fig)

# Plotting closing price, 100-day MA, and 200-day MA
st.subheader('Closing Price vs Time Chart with 100MA and 200MA')
fig = plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Close'], label='Close Price')
plt.plot(df.index, df['100MA'], label='100-Day Moving Average', color='orange')
plt.plot(df.index, df['200MA'], label='200-Day Moving Average', color='red')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title(f'{user_input} Closing Price with Moving Averages')
plt.legend()
st.pyplot(fig)

# Splitting data into training and testing
data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):])

# Scaling the data
scaler = MinMaxScaler(feature_range=(0,1))
data_training_array = scaler.fit_transform(data_training)

# Load the model
model = load_model('keras_model.h5')

# Prepare data for prediction
past_100_days = data_training.tail(100)
final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
input_data = scaler.transform(final_df)  # Use transform instead of fit_transform

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)

# Make predictions
y_predicted = model.predict(x_test)

# Inverse scale the predictions
scaler = scaler.scale_
scale_factor = 1 / scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

# Plotting predictions vs original prices
st.subheader('Predictions vs Original')
fig2 = plt.figure(figsize=(12, 6))
plt.plot(y_test, 'b', label='Original Price')
plt.plot(y_predicted, 'r', label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)
