


######--------------------page - setup-------------------------------#########

st.set_page_config(page_title="COVID-19 WORLD VACCINATION PROGRESS VISUALIZATION",
                    page_icon="🏥", 
                    layout="wide")
st.sidebar.header('<i>Covid-19 World Vaccination Progress Visualization</i>',anchor="vaccination progress",)
img=Image.open("image\download.jpg")
st.sidebar.image(img,width=300)
st.sidebar.subheader("Unvariant analysis (change over time)")

######---------------------------header------------------------------#########
with st.spinner("Loading Data..."):
    st.markdown("""
        <style>
            .mainhead{
                font-family: Courgette ,Book Antiqua ;
                #letter-spacing:.1px;
                word-spacing:1px;
                color :#0000FF; 
                text-shadow: 1px -1px 1px white, 1px -1px 2px white;
                font-size:40px;
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

######---------------------------header------------------------------#########
with st.spinner("Loading Data..."):
    st.markdown("""
        <style>
            .mainhead{
                font-family: Courgette ,Book Antiqua ;
                #letter-spacing:.1px;
                word-spacing:1px;
                color :#e67363; 
                text-shadow: 1px -1px 1px white, 1px -1px 2px white;
                font-size:40px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            .detail{
                font-size:18px;
                letter-spacing:.1px;
                word-spacing:1px;
                font-family:Calibri;
                color:#74cb35;
                display:inline-block;
                }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="mainhead"> Analysis of Best Selling Books </h1> <img src="" />',

     unsafe_allow_html=True)
    col1, col2 = st.beta_columns([5, 10])

    with col1:

        st.image('images/4.gif')

    with col2:

        col = st.beta_container()

        with col:
            st.markdown("""
                <style>
                    .content{
                    margin-top: 10%;
                    letter-spacing:.1px;
                    word-spacing:1px;
                    color:indianred;
                    margin-left:5%;}
                </style>
            """, unsafe_allow_html=True)

            st.markdown('<p class="content">Hey  There! <br> Welcome To My Project.This Project is all about Analyzing the Top BestSelling Books of Year 2009 to 2019.<br>We will be analyzing the Best Books on the basis of Reviews, Price, Rating, and the Author who had written it.<br>Our motive is to give you best idea about the trend going on. What people are liking and What they want to read in future. <br>One last tip, if you are on a mobile device, switch over to landscape for viewing ease. Give it a go! </p>', unsafe_allow_html=True)
            st.markdown(
                '<p class="content" style = "float:right;"> Made By Kavya Srivastava</p>', unsafe_allow_html=True)

st.markdown("")
st.markdown("___")
#data set ----------------------------------------------------------------detail
df=pd.read_csv("dataset\country_vaccinations.csv",parse_dates=['date'],dayfirst=True,index_col='date')
df.drop(['iso_code','vaccines','source_name','source_website'],axis=1,inplace=True)
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
        st.markdown('<p class="head"> DataSet Used In This Project  </p>',unsafe_allow_html=True)
        st.sidebar.markdown('<p class="content">This dataset is belongs to vaccination progress of different countries from 02-12-2020 till now.</p>',unsafe_allow_html=True)
        st.dataframe(df)
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

cols=['total_vaccinations',
 'people_vaccinated',
 'people_fully_vaccinated',
 'daily_vaccinations_raw',
 'daily_vaccinations',
 'total_vaccinations_per_hundred',
 'people_vaccinated_per_hundred',
 'people_fully_vaccinated_per_hundred',
 'daily_vaccinations_per_million']

col=st.sidebar.selectbox("select a column ",cols)
range=st.sidebar.selectbox("select a range to display",['D','3D','W','2W','M','2M'])
sub_df=df[col].resample(range).mean()
c=st.beta_columns(2)
c[0].write(sub_df)
fig=px.bar(sub_df,x=sub_df.index,y=col)
c[1].plotly_chart(fig)