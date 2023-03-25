# We have to import Liberaries

import streamlit as st
import pandas as pd
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff



# Import the Dataset
df=pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = helper.preprocessor(df, region_df)
# Receive df from Preprocessor

st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Olympic_rings_with_transparent_rims.svg/2560px-Olympic_rings_with_transparent_rims.svg.png')
st.sidebar.title("Olympics Analysis till 2016")
# Create Sidebar using streamlit Framework
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athelete-wise Analysis')
)
#st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,Country = helper.Country_year_list(df)
    select_year = st.sidebar.selectbox("Select Year",years)
    select_country = st.sidebar.selectbox("Select Country",Country)

    Region_list = df['Season'].dropna().unique().tolist()
    selected_country = st.sidebar.selectbox("Select the Country",Region_list)

    MedalTally = helper.fetch_medal_tally(df,select_year,select_country)
    if select_country=='Overall' and select_year=='Overall':
        st.header('Overall Medal Tally of All Countries ')

    if select_country!='Overall' and select_year=='Overall':
        st.header('Overall Medal Tally of '+ str(select_country) + " in Olympics")

    if select_country=='Overall' and select_year!='Overall':
        st.header('Overall Medal Tally of '+ str(select_year) + ' Olympics')

    if select_country!='Overall' and select_year!='Overall':
        st.header(str(select_country)+" Medal Tally in "+str(select_year)+" Olympics")

    st.table(MedalTally)



if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['Region'].unique().shape[0]

    st.title("Top Statistics of Olympic")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Cities")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Nations")
        st.title(nations)
    with col2:
        st.header("Events")
        st.title(events)

    with col3:
        st.header("Athelets")
        st.title(athletes)

    st.title("Participating Nations Over Editions")
    nations_over_time = helper.Participating_nation_over_time(df)
    fig = px.line(nations_over_time, x="Edition", y="No. of Nations")
    st.plotly_chart(fig)

    st.title("No. of Sports Over Editions")
    Sports_over_time = helper.Count_Sports_over_time(df)
    fig = px.bar(Sports_over_time, x="Edition", y="No. of Events")
    st.plotly_chart(fig)

    st.title("No. of Events Over Editions")
    Events_over_time = helper.Participating_Events_over_time(df)
    fig = px.area(Events_over_time, x="Edition", y="No. of Events")
    st.plotly_chart(fig)

    st.title("No. of Athletes Over Editions")
    athletes_over_time = helper.Count_athletes_over_time(df)
    fig = px.line(athletes_over_time, x="Edition", y="No. of Athletes")
    st.plotly_chart(fig)


    st.title('No. of Events Over Editions(Every Sports')
    # Next we have to draw a Heatmap, in which we give the No. of all Events for Every Sport over the Olympic Editions
    fig = plt.figure(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)


    st.title("Most Successfull Atheletes")
    Sport_list = df['Sport'].unique().tolist()
    Sport_list.sort()
    Sport_list.insert(0,'Overall')

    selected_sport = st.selectbox("Select the Sport",Sport_list)
    x = helper.most_successful_player(df,selected_sport)
    st.table(x)

    # Task - 1: Countrywise medal tally per year(line plot).

if user_menu == 'Country-wise Analysis':

    st.sidebar.title("Medal Analysis")
    Region_list = df['Region'].dropna().unique().tolist()
    Region_list.sort()

    selected_country = st.sidebar.selectbox("Select the Country",Region_list)

    country_df = helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country+" Medal Tally Over the Years")
    st.plotly_chart(fig)


    st.title(selected_country+ " Excels in the following Sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig,ax= plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athelet of "+selected_country)
    top10_df = helper.most_successfull_athelet_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athelete-wise Analysis':
    st.title('Age Distribution of Medlist')
    athelet_df = df.drop_duplicates(subset=['Name', 'Region'])
    x1 = athelet_df['Age'].dropna()
    x2 = athelet_df[athelet_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelet_df[athelet_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelet_df[athelet_df['Medal'] == 'Bronze']['Age'].dropna()


    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                       show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)

    # Male vs Female Participation Graph in Olympic
    st.title("Men Vs Women Participation Over the Years")
    final = helper.Men_v_Women_Participation(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    st.plotly_chart(fig)

    #st.title("Age Distribution for Each Game wrt Gold Medlist")
    # x = []
    # name = []
    # famous_sports = ['Basketball','Judo','Football','Tug-of-War','Atheletics',
    #                  'Swimming','Badminton','Sailing','Gymnastics','Art Competetions',
    #                  'Handball','Weightlifting','Wrestling','Water Polo',
    #                  'Hockey','Rowing','Fencing','Shooting','Boxing','Taekwondo',
    #                  'Cycling','Diving','Canoeing','Tennis','Golf','Softball',
    #                  'Archery','Volleyball','Synchronized Swimming','Table Tennis',
    #                  'Baseball','Rhythmic Gymnastics','Rugby Sevens',
    #                  'Beach Volleyball','Triathon','Rugby','Polo','Ice Hockey']
    # for sports in famous_sports:
    #     temp_df = athelet_df[athelet_df['Sport']==sports]
    #     x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
    #     name.append(sports)

    # fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    # fig.update_layout(autosize=False,width=1000,height=600)
    # st.plotly_chart(fig)




# # Athelete Wise Analysis Graph-3
#     Sport_list = df['Sport'].unique().tolist()
#     Sport_list.sort()
#     Sport_list.insert(0, 'Overall')

#     selected_sport = st.selectbox("Select the Sport", Sport_list)
#     temp_df = helper.weight_v_height(df,selected_sport)
#     fig,ax = plt.subplots()
#     ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
#     st.pyplot(fig)








st.text('@2023 All Rights Reserved-atobtech.blogsport.com')


