import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from matplotlib import pyplot as plt
plt.style.use('ggplot')

import seaborn as sns # for making plots with seaborn
color = sns.color_palette()
sns.set(rc={'figure.figsize':(25,15)})

import plotly
import plotly.graph_objs as go
import plotly.figure_factory as ff
import cufflinks as cf
import scipy.stats as stats

st.set_page_config(page_title="DATA ANALYSIS ON ANDRIOD APP DATASET", page_icon="🏥", layout="wide")
img = ("Images\img_1.jpg")
st.sidebar.image(img, width=200)

@st.cache
def load_data():
    df = pd.read_csv('data/googleplaystore.csv')

    df.drop_duplicates(subset='App', inplace=True)
    df = df[df['Android Ver'] != np.nan]
    df = df[df['Android Ver'] != 'NaN']
    df = df[df['Installs'] != 'Free']
    df = df[df['Installs'] != 'Paid']

    df['Installs'] = df['Installs'].apply(lambda x: x.replace('+', '') if '+' in str(x) else x)
    df['Installs'] = df['Installs'].apply(lambda x: x.replace(',', '') if ',' in str(x) else x)
    df['Installs'] = df['Installs'].apply(lambda x: int(x))

    df['Size'] = df['Size'].apply(lambda x: str(x).replace('Varies with device', 'NaN') if 'Varies with device' in str(x) else x)
    df['Size'] = df['Size'].apply(lambda x: str(x).replace('M', '') if 'M' in str(x) else x)
    df['Size'] = df['Size'].apply(lambda x: str(x).replace(',', '') if 'M' in str(x) else x)
    df['Size'] = df['Size'].apply(lambda x: float(str(x).replace('k', '')) / 1000 if 'k' in str(x) else x)
    df['Size'] = df['Size'].apply(lambda x: float(x))

    df['Installs'] = df['Installs'].apply(lambda x: float(x))

    df['Price'] = df['Price'].apply(lambda x: str(x).replace('$', '') if '$' in str(x) else str(x))
    df['Price'] = df['Price'].apply(lambda x: float(x))

    df['Reviews'] = df['Reviews'].apply(lambda x: int(x))
    return df

df = load_data()
reviews_df = pd.read_csv(r'data/googleplaystore_user_reviews.csv')

def home(title):
    st.title(title)
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

    st.markdown('<h1 class="mainhead"> <i>DATA ANALYSIS ON ANDROID APP DATASET</i> </h1>',
                unsafe_allow_html=True)
    col1, col2 = st.beta_columns([5, 10])
    with col1:
        st.image('Images\Gif_1.gif', use_column_width=True)
    with col2:
        col = st.beta_container()
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

            st.markdown(
                '<p class="content" style="float:right">MADE BY VAISHALI DIXIT</P>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown("_______")


def page1(title):
    st.title(title)
    x = st.sidebar.slider("Choose how many rows to show", min_value=0, value=10, max_value=df.shape[0])
    st.header("Raw Data")
    st.write(df.head(x))
    st.markdown("---")
    st.success(f"Number of Apps in the dataset: {len(df)}")
    st.markdown("---")
    st.header("DataSet Summary")
    st.write(df.describe())

def page2(title):
    st.title(title)
    st.header("Basic EDA")
    x = df['Rating'].dropna()
    y = df['Size'].dropna()
    z = df['Installs'][df.Installs!=0].dropna()
    p = df['Reviews'][df.Reviews!=0].dropna()
    t = df['Type'].dropna()
    price = df['Price']
    p = sns.pairplot(pd.DataFrame(list(zip(x, y, np.log(z), np.log10(p), t, price)), 
                            columns=['Rating','Size', 'Installs', 'Reviews', 'Type', 'Price']), hue='Type', palette="Set2")
    st.pyplot(p)
    st.info("This is the basic exploratory analysis to look for any evident patterns or relationships between the features.")
    st.markdown("---")
    st.header("Android Market Breakdown")
    number_of_apps_in_category = df['Category'].value_counts().sort_values(ascending=True)
    st.subheader("Which category has the highest share of (active) apps in the market?")
    data = px.pie(
            labels = number_of_apps_in_category.index,
            values = number_of_apps_in_category.values)
    st.plotly_chart(data)
    st.info("Family and Game apps have the highest market prevelance.\nInterestingly, Tools, Business and Medical apps are also catching up.")
    st.markdown("---")
    st.header("Average rating of apps")
    st.subheader("Do any apps perform really good or really bad?")
    data = px.histogram(x = df.Rating)
    st.plotly_chart(data)
    st.info("Generally, most apps do well with an average rating of 4.17.\n"+
            "\nLet's break this down and inspect if we have categories which perform exceptionally good or bad.")
    st.markdown("---")
    st.header("App ratings across categories - One Way Anova Test")
    f = stats.f_oneway(df.loc[df.Category == 'BUSINESS']['Rating'].dropna(), 
               df.loc[df.Category == 'FAMILY']['Rating'].dropna(),
               df.loc[df.Category == 'GAME']['Rating'].dropna(),
               df.loc[df.Category == 'PERSONALIZATION']['Rating'].dropna(),
               df.loc[df.Category == 'LIFESTYLE']['Rating'].dropna(),
               df.loc[df.Category == 'FINANCE']['Rating'].dropna(),
               df.loc[df.Category == 'EDUCATION']['Rating'].dropna(),
               df.loc[df.Category == 'MEDICAL']['Rating'].dropna(),
               df.loc[df.Category == 'TOOLS']['Rating'].dropna(),
               df.loc[df.Category == 'PRODUCTIVITY']['Rating'].dropna()
              )

    groups = df.groupby('Category').filter(lambda x: len(x) > 286).reset_index()
    array = groups['Rating'].hist(by=groups['Category'], sharex=True, figsize=(20,20))
    st.image(r"Images\__results___19_1.png")
    st.info("The average app ratings across categories is significantly different.")
    st.markdown("---")
    groups = df.groupby('Category').filter(lambda x: len(x) >= 170).reset_index()
    #print(type(groups.item.['BUSINESS']))
    print('Average rating = ', np.nanmean(list(groups.Rating)))
    #print(len(groups.loc[df.Category == 'DATING']))
    c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 720, len(set(groups.Category)))]
    layout = {'title' : 'App ratings across major categories',
            'xaxis': {'tickangle':-40},
            'yaxis': {'title': 'Rating'},
              'plot_bgcolor': 'rgb(250,250,250)',
              'shapes': [{
                  'type' :'line',
                  'x0': -.5,
                  'y0': np.nanmean(list(groups.Rating)),
                  'x1': 19,
                  'y1': np.nanmean(list(groups.Rating)),
                  'line': { 'dash': 'dashdot'}
              }]
              }

    data = [{
        'y': df.loc[df.Category==category]['Rating'], 
        'type':'violin',
        'name' : category,
        'showlegend':False,
        #'marker': {'color': 'Set2'},
        } for i,category in enumerate(list(set(groups.Category)))]
    st.plotly_chart(go.Figure(data=data, layout=layout))
    st.info("Almost all app categories perform decently."+
            " Health and Fitness and Books and Reference produce the highest quality apps with 50% apps having a rating greater than 4.5. This is extremely high!"+
            "\n\nOn the contrary, 50% of apps in the Dating category have a rating lesser than the average rating."+
            "\n\nA few junk apps also exist in the Lifestyle, Family and Finance category.")
    st.markdown("---")
    st.header("Sizing Strategy - Light Vs Bulky?")
    st.subheader("How do app sizes impact the app rating?")
    groups = df.groupby('Category').filter(lambda x: len(x) >= 50).reset_index()
    sns.set_style("darkgrid")
    ax = sns.jointplot(df['Size'], df['Rating'])
    st.pyplot(ax)
    st.info("Most top rated apps are optimally sized between ~2MB to ~40MB - neither too light nor too heavy.")
    c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, len(list(set(groups.Category))))]
    subset_df = df[df.Size > 40]
    groups_temp = subset_df.groupby('Category').filter(lambda x: len(x) >20)

    # for category in enumerate(list(set(groups_temp.Category))):
    #     print (category)

    data = [{
        'x': groups_temp.loc[subset_df.Category==category[1]]['Rating'], 
        'type':'scatter',
        'y' : subset_df['Size'],
        'name' : str(category[1]),
        'mode' : 'markers',
        'showlegend': True,
        #'marker': {'color':c[i]}
        #'text' : df['rating'],
        } for category in enumerate(['GAME', 'FAMILY'])]


    layout = {'title':"Rating vs Size", 
              'xaxis': {'title' : 'Rating'},
              'yaxis' : {'title' : 'Size (in MB)'},
             'plot_bgcolor': 'rgb(0,0,0)'}
    st.plotly_chart(go.Figure(data=data, layout=layout))
    st.info("Most bulky apps ( >50MB) belong to the Game and Family category. Despite this, these bulky apps are fairly highly rated indicating that they are bulky for a purpose.")

def page3(title):
    st.title(title)
    st.header("Pricing Strategy - Free Vs Paid?")
    st.subheader("How do app prices impact app rating?")
    paid_apps = df[df.Price>0]
    p = sns.jointplot( "Price", "Rating", paid_apps)
    st.pyplot(p)
    st.info("Most top rated apps are optimally priced between ~1 𝑡𝑜 30 . There are only a very few apps priced above 20$.")
    st.markdown("---")
    st.header("Current pricing trend - How to price your app?")
    subset_df = df[df.Category.isin(['GAME', 'FAMILY', 'PHOTOGRAPHY', 'MEDICAL', 'TOOLS', 'FINANCE',
                                 'LIFESTYLE','BUSINESS'])]
    sns.set_style('darkgrid')
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 8)
    p = sns.stripplot(x="Price", y="Category", data=subset_df, jitter=True, linewidth=1)
    title = ax.set_title('App pricing trend across categories')
    st.pyplot(fig)
    st.info("*Shocking...Apps priced above 250$ !!! *")
    st.markdown("---")
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 8)
    subset_df_price = subset_df[subset_df.Price<100]
    p = sns.stripplot(x="Price", y="Category", data=subset_df_price, jitter=True, linewidth=1)
    title = ax.set_title('App pricing trend across categories - after filtering for junk apps')
    st.pyplot(fig)
    st.info("Clearly, Medical and Family apps are the most expensive. Some medical apps extend even upto 80$.\n\n"+
            "\nAll other apps are priced under 30$.\n\n"+
            "\nSurprisingly, all game apps are reasonably priced below 20$.")
    st.markdown("---")

    st.header("Distribution of paid and free apps across categories")
    new_df = df.groupby(['Category', 'Type']).agg({'App' : 'count'}).reset_index()

    outer_group_names = ['GAME', 'FAMILY', 'MEDICAL', 'TOOLS']
    outer_group_values = [len(df.App[df.Category == category]) for category in outer_group_names]

    a, b, c, d=[plt.cm.Blues, plt.cm.Reds, plt.cm.Greens, plt.cm.Purples]


    inner_group_names = ['Paid', 'Free'] * 4
    inner_group_values = []

    for category in outer_group_names:
        for t in ['Paid', 'Free']:
            x = new_df[new_df.Category == category]
            try:
                inner_group_values.append(int(x.App[x.Type == t].values[0]))
            except:
                inner_group_values.append(0)

    explode = (0.025,0.025,0.025,0.025)
    # First Ring (outside)
    fig, ax = plt.subplots(figsize=(10,10))
    ax.axis('equal')
    mypie, texts, _ = ax.pie(outer_group_values, radius=1.2, labels=outer_group_names, autopct='%1.1f%%', pctdistance=1.1,
                                     labeldistance= 0.75,  explode = explode, colors=[a(0.6), b(0.6), c(0.6), d(0.6)], textprops={'fontsize': 16})
    plt.setp( mypie, width=0.5, edgecolor='black')
     
    # Second Ring (Inside)
    mypie2, _ = ax.pie(inner_group_values, radius=1.2-0.5, labels=inner_group_names, labeldistance= 0.7, 
                       textprops={'fontsize': 12}, colors = [a(0.4), a(0.2), b(0.4), b(0.2), c(0.4), c(0.2), d(0.4), d(0.2)])
    plt.setp( mypie2, width=0.5, edgecolor='black')
    st.pyplot(plt)
    st.info("Distribution of free and paid apps across major categories")
    st.markdown("---")
    st.header("Are paid apps downloaded as much as free apps?")
    trace0 = go.Box(
    y=np.log10(df['Installs'][df.Type=='Paid']),
    name = 'Paid',
    marker = dict(
            color = 'rgb(214, 12, 140)',
        )
    )
    trace1 = go.Box(
        y=np.log10(df['Installs'][df.Type=='Free']),
        name = 'Free',
        marker = dict(
            color = 'rgb(0, 128, 128)',
        )
    )
    layout = go.Layout(
        title = "Number of downloads of paid apps Vs free apps",
        yaxis= {'title': 'Number of downloads (log-scaled)'}
    )
    data = [trace0, trace1]
    st.plotly_chart(go.Figure(data=data, layout=layout))
    st.info("Paid apps have a relatively lower number of downloads than free apps. However, it is not too bad.")
    st.markdown("---")
    st.header("How do the sizes of paid apps and free apps vary?")
    temp_df = df[df.Type == 'Paid']
    temp_df = temp_df[temp_df.Size > 5]
    #type_groups = df.groupby('Type')

    data = [{
        #'x': type_groups.get_group(t)['Rating'], 
        'x' : temp_df['Rating'],
        'type':'scatter',
        'y' : temp_df['Size'],
        #'name' : t,
        'mode' : 'markers',
        #'showlegend': True,
        'text' : df['Size'],
        } for t in set(temp_df.Type)]


    layout = {'title':"Rating vs Size", 
              'xaxis': {'title' : 'Rating'},
              'yaxis' : {'title' : 'Size (in MB)'},
             'plot_bgcolor': 'rgb(0,0,0)'}
    st.plotly_chart(go.Figure(data=data, layout=layout))
    st.info("Majority of the paid apps that are highly rated have small sizes. "+
            "This means that most paid apps are designed and developed to cater to specific functionalities and hence are not bulky."+
            "\n\nUsers prefer to pay for apps that are light-weighted. A paid app that is bulky may not perform well in the market.")
    st.markdown("---")
    

def page4(title):
    st.title(title)
    st.markdown("")
    st.header("Exploring Correlations")
    corrmat = df.corr()
    f, ax = plt.subplots()
    p = sns.heatmap(corrmat, annot=True, cmap=sns.diverging_palette(220, 20, as_cmap=True))
    st.pyplot(f)
    st.markdown("---")
    df_copy = df.copy()

    df_copy = df_copy[df_copy.Reviews > 10]
    df_copy = df_copy[df_copy.Installs > 0]

    df_copy['Installs'] = np.log10(df['Installs'])
    df_copy['Reviews'] = np.log10(df['Reviews'])

    fig = sns.lmplot("Reviews", "Installs", data=df_copy)
    ax = plt.gca()
    _ = ax.set_title('Number of Reviews Vs Number of Downloads (Log scaled)')
    st.pyplot(fig)
    st.info("""A moderate positive correlation of 0.63 exists between the number of reviews and number of downloads. This means that customers tend to download a given app more if it has been reviewed by a larger number of people.

This also means that many active users who download an app usually also leave back a review or feedback.

So, getting your app reviewed by more people maybe a good idea to increase your app's capture in the market!""")
    st.markdown("---")
    merged_df = pd.merge(df, reviews_df, on = "App", how = "inner")
    merged_df = merged_df.dropna(subset=['Sentiment', 'Translated_Review'])
    grouped_sentiment_category_count = merged_df.groupby(['Category', 'Sentiment']).agg({'App': 'count'}).reset_index()
    grouped_sentiment_category_sum = merged_df.groupby(['Category']).agg({'Sentiment': 'count'}).reset_index()

    new_df = pd.merge(grouped_sentiment_category_count, grouped_sentiment_category_sum, on=["Category"])
    #print(new_df)
    new_df['Sentiment_Normalized'] = new_df.App/new_df.Sentiment_y
    new_df = new_df.groupby('Category').filter(lambda x: len(x) ==3)
    # new_df = new_df[new_df.Category.isin(['HEALTH_AND_FITNESS', 'GAME', 'FAMILY', 'EDUCATION', 'COMMUNICATION', 
    #                                      'ENTERTAINMENT', 'TOOLS', 'SOCIAL', 'TRAVEL_AND_LOCAL'])]
    new_df

    trace1 = go.Bar(
        x=list(new_df.Category[::3])[6:-5],
        y= new_df.Sentiment_Normalized[::3][6:-5],
        name='Negative',
        marker=dict(color = 'rgb(209,49,20)')
    )

    trace2 = go.Bar(
        x=list(new_df.Category[::3])[6:-5],
        y= new_df.Sentiment_Normalized[1::3][6:-5],
        name='Neutral',
        marker=dict(color = 'rgb(49,130,189)')
    )

    trace3 = go.Bar(
        x=list(new_df.Category[::3])[6:-5],
        y= new_df.Sentiment_Normalized[2::3][6:-5],
        name='Positive',
        marker=dict(color = 'rgb(49,189,120)')
    )

    data = [trace1, trace2, trace3]
    layout = go.Layout(
        title = 'Sentiment analysis',
        barmode='stack',
        xaxis = {'tickangle': -45},
        yaxis = {'title': 'Fraction of reviews'}
    )

    fig = go.Figure(data=data, layout=layout)
    st.header("Basic sentiment analysis - User reviews")
    st.plotly_chart(fig)
    st.info("""Health and Fitness apps perform the best, having more than 85% positive reviews.
On the contrary, many Game and Social apps perform bad leading to 50% positive and 50% negative.""")
    st.markdown("---")
    sns.set_style('ticks')
    sns.set_style("darkgrid")
    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27)
    ax = sns.boxplot(x='Type', y='Sentiment_Polarity', data=merged_df)
    title = ax.set_title('Sentiment Polarity Distribution')
    st.pyplot(fig)
    st.info("""Free apps receive a lot of harsh comments which are indicated as outliers on the negative Y-axis.

Users are more lenient and tolerant while reviewing paid apps - moderate choice of words. They are never extremely negative while reviewing a paid app.""")
    st.markdown("---")

def conclusion(title):
    st.title(title)
    st.markdown("""
 - Average rating of (active) apps on Google Play Store is **4.17**.
 
 
 - **Users prefer to pay for apps that are light-weighted.** Thus, a paid app that is bulky may not perform well in the market.
 
 
 - Most of the top rated apps are **optimally sized between ~2MB to ~40MB** - neither too light nor too heavy.
 
 
 - Most of the top rated apps are **optimally priced between ~1\$ to ~30\$** - neither too cheap nor too expensive.
 
 
 - **Medical and Family apps are the most expensive** and even extend upto 80\$.
 
 
 - Users tend to download a given app more if it has been reviewed by a large number of people.
 
 
 - **Health and Fitness** apps receive more than **85% positive reviews**. **Game and Social** apps receive mixed feedback - **50% positive and 50% negative.**
 
 
 - **Users are more grim and harsh while reviewing free apps** than paid apps. 
""")

pages = {
    "Introduction": home,
    "Show Raw data": page1,
    "Data Exploration": page2,
    "According to Price": page3,
    "According to Reviews": page4,
    "Conclusion": conclusion
         }
page = st.sidebar.selectbox("Choose a page..", list(pages.keys()))
pages[page](page)
