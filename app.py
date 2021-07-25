from seaborn.categorical import barplot
from datetime import datetime
from re import U
import streamlit as st
import pandas as pd           #data processing ,csv file i/o eg->pd.read_csv
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

######--------------------page - setup-------------------------------#########

st.set_page_config(page_title="DATA ANALYSIS ON ANDRIOD APP DATASET",
                    page_icon="🏥", 
                    layout="wide")
st.sidebar.header('<i>DATA ANALYSIS ON ANDRIOD APP DATASET</i>',anchor="analysis on andriod app",)
img=("Images\img_1.jpg")
st.sidebar.image(img,width=200)
st.sidebar.subheader("Unvariant analysis (change over time)")

######---------------------------header------------------------------#########


with st.spinner("Loading Data......"):
    st.markdown("""
        <style>
            .mainhead{
                font-family: Courgette ,Book Antiqua ;
                #letter-spacing:.1px;
                word-spacing:1px;
                color :#0000FF; 
                text-shadow: 1px -1px 1px white, 1px -1px 2px white;
                font-size:50px;
                    }
        </style>
    """, unsafe_allow_html=True)

with st.spinner("loading data...."):
   st.markdown("""
        <style>
            .detail{
                    font-size:20px;
                    letter-spacing:.1px;
                    word-spacing:1px;
                    font-family:Calibri;
                    color:#e67363;
                    display:inline-block;
                    }
        </style>
         """, unsafe_allow_html=True)

st.markdown('<h1 class="mainhead"> <i>DATA ANALYSIS ON ANDROID APP DATASET</i> </h1>',unsafe_allow_html=True)
col1,col2=st.beta_columns([5,10])
with col1:
    st.image('Images\Gif_1.gif',width=325)
with col2:
    col=st.beta_container()
    with col:
        st.markdown("""
                    <style>
                        .content{   
                                    margin-top:-3%;
                                    letter-spacing:.1px;
                                    word-spacing:1px;
                                    color: #00008B;
                                    margin-left:8%;}
                    </style>
                    """, unsafe_allow_html=True)
        
        st.markdown('<p class="content">Hey There ! Welcome To My Project.This Project is all about Data Analysis on Andriod App of Year till 2018.<br>We will be analyzing the Best Andriod App on the basis of Reviews, Price, Rating, and the Catagory.<br>Our motive is to give you best idea about the trend going on. What people are liking and What they want to read in future. <br>One last tip, if you are on a mobile device, switch over to landscape for viewing ease. Give it a go! </p>', unsafe_allow_html=True)
                    
        st.markdown('<p class="content" style="float:right">MADE BY VAISHALI DIXIT</P>',unsafe_allow_html=True)

st.markdown("")
st.markdown("_______")

#data set ----------------------------------------------------------------detail
df=pd.read_csv("data\googleplaystore.csv")
df.drop(['App',
 'Category',
 'Rating',
 'Reviews',
 'Size',
 'Installs',
 'Price'],axis=1,inplace=True)
df.fillna(value=0,inplace=True)

st.markdown(""" 
            <style>
                .head{
                    font-family: Calibri, Book Antiqua; 
                    font-size:4vh;
                    padding-top:2%;
                    padding-bottom:2%;
                    font-weight:light;
                    color:#ffc68a;
                    #text-align:center;
                    
                    }
            </style>
            """, unsafe_allow_html=True)
@st.cache(suppress_st_warning=True)
def viewDataset(pathlist):
    with st.spinner("loading data....."):
        st.markdown("")

if st.sidebar.checkbox('View Dataset'):
        st.markdown('<p class="head"> DataSet Used In This Project </p>',unsafe_allow_html=True)
        st.sidebar.markdown('<p class="content"><i>This dataset is belongs to analysis on andriod app of different countries from 07-01-2018.</i></p>',unsafe_allow_html=True)
        st.dataframe(df)

if st.sidebar.checkbox('Show dataset details'):        
    st.markdown(""" 
                <style>
                    .block{
                            font-family: Book Antiqua; 
                            font-size:24px;
                            padding-top:11%;
                            font-weight:light;
                            color:darkblue;
                        }
                </style>
                    """, unsafe_allow_html=True)


    cols = st.beta_columns(4)
    cols[0].markdown(
                '<p class="block"> Number of Rows : <br> </p>', unsafe_allow_html=True)
    cols[1].markdown(f"# {df.shape[0]}")
    cols[2].markdown(
                '<p class= "block"> Number of Columns : <br></p>', unsafe_allow_html=True)
    cols[3].markdown(f"# {df.shape[1]}")
    st.markdown('---')

    st.markdown('<p class= "head"> Summary </p>', unsafe_allow_html=True)
    st.markdown("")
    st.dataframe(df.describe())
    st.markdown('---')

    types = {'object': 'Categorical',
                    'int64': 'Numerical', 'float64': 'Numerical'}
    types = list(map(lambda t: types[str(t)], df.dtypes))
    st.markdown('<p class="head">Dataset Columns</p>',
                        unsafe_allow_html=True)
    for col, t in zip(df.columns, types):
                st.markdown(f"## {col}")
                cols = st.beta_columns(4)
                cols[0].markdown('#### Unique Values :')
                cols[1].markdown(f"## {df[col].unique().size}")
                cols[2].markdown('#### Type :')
                cols[3].markdown(f"## {t}")
                st.markdown("___")
    
    ### column selection 
st.sidebar.subheader("Univariate analysis (change over time)")


col=st.sidebar.selectbox("select a column ",df.columns.tolist())


st.sidebar.subheader("Bivariate analysis")
cols=['App',
 'Category',
 'Rating',
 'Reviews',
 'Size',
 'Installs',
 'Price',]
 

selection =st.sidebar.multiselect("select two columns ",cols)
if len(selection) == 2:
    fig = px.scatter(df,x=selection[0],y=selection[1])
    cols = st.beta_columns(2)
    cols[0].write(df[[selection[0],selection[1]]])
    cols[1].plotly_chart(fig,use_container_width=True)

st.sidebar.subheader("comparison plots")
cols =st.sidebar.multiselect("select two columns ",df.columns.tolist())
kind =st.sidebar.selectbox("select plot type",['area','line','bar','box','hist'])
if len(cols) >= 2:
    fig,ax = plt.subplots(figsize=(7,5))
    c = st.beta_columns(2)
    c[0].write(df[cols].resample('W').count())
    df[cols].resample('W').sum().plot(kind=kind,ax=ax,legend=True,title=f"{cols[0]} vs {cols[1]}")
    c[1].pyplot(fig)


st.sidebar.subheader("maps plot")
cols=st.sidebar.multiselect("select two columns",df.columns.tolist())
kind =st.sidebar.selectbox("select plot type",['area','line','bar','box','hist'])
if len(cols) >= 2:
    fig,ax = plt.subplots(figsize=(7,5))
    c = st.beta_columns(2)
    c[0].write(df[cols].resample('W').count())
    df[cols].resample('W').sum().plot(kind=kind,ax=ax,legend=True,title=f"{cols[0]} vs {cols[1]}")
    c[1].pyplot(fig)


st.sidebar.subheader("maps plot")
cols=st.sidebar.multiselect("select two columns",df.columns.tolist())
    
    
    
