import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st


def load_data():
    return pd.read_csv('data/googleplaystore.csv')

st.set_page_config(layout="wide")
df = load_data()

st.title("data analysis on andriod app dataset")

st.sidebar.subheader("change over time (Univariate analysis)")
cols = ['App','Category','Rating','Size','Installs','Type','Price','Content Rating','Genres','Last Updated','Current Ver''Android Ver']
 
col = st.sidebar.selectbox("select a column",cols)

fig = px.line(df, x=df.index, y=col,)
st.plotly_chart(fig,use_container_width=True)