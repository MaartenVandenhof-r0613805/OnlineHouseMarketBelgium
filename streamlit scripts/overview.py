import streamlit as st
import pandas as pd
import numpy as np


## Import data
@st.cache
def get_data():
    data = pd.read_excel("data/appartments.xlsx")
    if data["total_price"].max() > 5000:
        return data, data["total_price"].min(), np.int64(5000)
    return data, data["total_price"].min(), data["total_price"].max()


app_df, min_price, max_price = get_data()

## Set Layout
with st.sidebar:
    locations = st.multiselect('Select city''', app_df['city'].unique())
    values = st.slider('Select price range''', value=(min_price.item(), max_price.item()))
    min_bedrooms = st.slider('Select minimum amount of bedrooms', app_df['bedrooms'].min().item(),
                             app_df['bedrooms'].max().item(), step=1.0)
    types = st.multiselect('Select housing types''', app_df['type'].unique())

## Show on webpage
if values[1] > 5000:
    filtered_df = app_df[app_df["total_price"].between(values[0], app_df["total_price"].max().item())
                        & app_df['city'].isin(locations)
                        & (app_df['bedrooms'] > min_bedrooms)
                        & app_df['type'].isin(types)]
else:
    filtered_df = app_df[app_df["total_price"].between(values[0], values[1])
                        & app_df['city'].isin(locations)
                        & (app_df['bedrooms'] > min_bedrooms)
                        & app_df['type'].isin(types)]


st.dataframe(filtered_df)

## Create cards
count  = 0
for _, row in filtered_df.iterrows():
    container = st.container()
    cols = container.columns(3)
    cols[0].write(''' ## Price:  ''')
    cols[0].write(''' ##### ''' + str(row['total_price']))
    cols[1].write(''' ## Bedrooms:  ''')
    cols[1].write(''' ##### ''' + str(row['bedrooms']))
    cols[2].write(''' ## Address:  ''')
    cols[2].write(''' ##### ''' + str(row['address']))
    count = count + 1
    if count > 30:
        break
