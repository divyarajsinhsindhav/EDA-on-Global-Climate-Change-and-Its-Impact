import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

# Load the data
df = pd.read_csv('data/GlobalLandTemperaturesByMajorCity.csv')

# Streamlit Title
st.title("Global Land Temperature Analysis")

st.subheader("Data Overview")
num_cities = df['City'].nunique()
# Extract the year from the 'dt' column
df['Year'] = pd.to_datetime(df['dt']).dt.year  # Ensure 'dt' column is in datetime format
year_min, year_max = df['Year'].min(), df['Year'].max()
st.write("Total number of unique cities:", num_cities)
st.write("Data covers years:", f"{year_min} - {year_max}")


# Impute missing values using the mean
df['AverageTemperature'].fillna(df['AverageTemperature'].mean(), inplace=True)
df['AverageTemperatureUncertainty'].fillna(df['AverageTemperatureUncertainty'].mean(), inplace=True)

# Group by Year and calculate the average temperature and uncertainty
yearly_data = df.groupby('Year')[['AverageTemperature', 'AverageTemperatureUncertainty']].mean().reset_index()

# Calculate the 10-year moving average
yearly_data['10_year_avg'] = yearly_data['AverageTemperature'].rolling(window=10).mean()

# Display the Yearly Data
st.subheader("Yearly Average Temperature & Uncertainty")
st.write(yearly_data.drop(columns=['10_year_avg']))

# Visualize Year vs Average Temperature using Plotly (Interactive Plot)
st.subheader("Year vs Average Temperature (Line Plot)")
fig_year_temp = px.line(yearly_data, x='Year', y='AverageTemperature', 
                        title="Yearly Average Temperature", 
                        labels={'AverageTemperature': 'Average Temperature (°C)', 'Year': 'Year'})
st.plotly_chart(fig_year_temp)

# Visualize 10 Year Moving Average Temperature using Plotly (Interactive Plot)
st.subheader("10 Year Moving Average Temperature")
fig_year_temp = px.line(yearly_data, x='Year', y='10_year_avg', 
                        title="10 Year Moving Average Temperature", 
                        labels={'10_year_avg': 'Average Temperature (°C)', 'Year': 'Year'})
st.plotly_chart(fig_year_temp)

# --------------- Yearly City Averages ------------------------

# Group by City and Year and calculate the average temperature for each city per year
city_yearly_data = df.groupby(['City', 'Year'])[['AverageTemperature']].mean().reset_index()

# Display the first few rows of the city yearly data
st.subheader("Yearly Average Temperature by City")
st.write(city_yearly_data.head())

# Select a city to display the yearly temperature data
city_list = city_yearly_data['City'].unique()
selected_city = st.selectbox("Select a City", city_list)

# Filter the data for the selected city
selected_city_data = city_yearly_data[city_yearly_data['City'] == selected_city]

# Visualize Yearly Temperature for the selected city using Plotly
st.subheader(f"Yearly Average Temperature for {selected_city}")
fig_city_temp = px.line(selected_city_data, x='Year', y='AverageTemperature', 
                        title=f"Yearly Average Temperature for {selected_city}", 
                        labels={'AverageTemperature': 'Average Temperature (°C)', 'Year': 'Year'})
st.plotly_chart(fig_city_temp)


