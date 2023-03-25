import numpy as np
import streamlit as st
import pandas as pd

def preprocessor(df,region_df):
    # Filtering the Summer Olympic ( If we want)
    df = pd.read_csv('athlete_events.csv')
    region_df = pd.read_csv('noc_regions.csv')
    Season_list = df['Season'].dropna().unique().tolist()
    selected_Season = st.selectbox("Select the Season",Season_list)
    df = df[df['Season']==selected_Season]

    # Merge with Region
    df = df.merge(region_df,on='NOC',how="left")
    # Dropping Duplicates
    df.drop_duplicates(inplace=True)
    # Encode the Medals in Separate Columns
    df = pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df

def MedalTally(df):

    MedalTally = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Season', 'Event', 'Medal'])

    MedalTally = MedalTally.groupby('Region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    MedalTally['Total'] = MedalTally['Gold'] + MedalTally['Silver'] + MedalTally['Bronze']

    MedalTally['Gold'] = MedalTally['Gold'].astype('int')
    MedalTally['Silver'] = MedalTally['Silver'].astype('int')
    MedalTally['Bronze'] = MedalTally['Bronze'].astype('int')
    MedalTally['Total'] = MedalTally['Total'].astype('int')

    return MedalTally

def Country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    Country = np.unique(df['Region'].dropna().values).tolist()
    Country.sort()
    Country.insert(0,'Overall')

    return years,Country


def fetch_medal_tally(df, years, Country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Season', 'Event', 'Medal'])
    flag = 0
    if years == 'Overall' and Country == 'Overall':
        temp_df = medal_df
    if years == 'Overall' and Country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['Region'] == Country]
    if years != 'Overall' and Country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(years)]
    if years != 'Overall' and Country != 'Overall':
        temp_df = medal_df[(medal_df['Region'] == Country) & (medal_df['Year'] == int(years))]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                    ascending=True).reset_index()
    else:
        x = temp_df.groupby('Region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()


    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Gold']+x['Silver'] + x['Bronze']
    x['Total'] = x['Total'].astype('int')

    return x


def Participating_nation_over_time(df):
    # No. of Participating Nations over the Years
    nations_over_time = df.drop_duplicates(['Year', 'Region'])['Year'].value_counts().reset_index().sort_values('index')
    # Rename the Columns
    nations_over_time.rename(columns={'index': 'Edition', 'Year': 'No. of Nations'}, inplace=True)
    return nations_over_time

def Participating_Events_over_time(df):
    # No. of Participating Nations over the Years
    Events_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('index')
    # Rename the Columns
    Events_over_time.rename(columns={'index': 'Edition', 'Year': 'No. of Events'}, inplace=True)
    return Events_over_time

def Count_Sports_over_time(df):
    # No. of Sports over Editions
    Sports_over_time=df.drop_duplicates(['Year', 'Sport'])['Year'].value_counts().reset_index().sort_values('index')
    # Rename the Columns
    Sports_over_time.rename(columns={'index': 'Edition', 'Year': 'No. of Events'}, inplace=True)
    return Sports_over_time

def Count_athletes_over_time(df):
    # No. of Sports over Editions
    athletes_over_time=df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values('index')
    # Rename the Columns
    athletes_over_time.rename(columns={'index': 'Edition', 'Year': 'No. of Athletes'}, inplace=True)
    return athletes_over_time


def most_successful_player(df, Sport):
    temp_df = df.dropna(subset=['Medal'])

    if (Sport != 'Overall'):
        temp_df = temp_df[temp_df['Sport'] == Sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'Region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def year_wise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['Region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['Region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int)
    return pt


# We have to find most successfull Atheletes in every country
def most_successfull_athelet_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['Region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name',"Region"])
    athlete_df['Medal'].fillna('Np Medal',inplace=True)
    if sport!='Overall':
        temp_df = athlete_df[athlete_df['Sport']==sport]
    else :
        return athlete_df
    return temp_df

def Men_v_Women_Participation(df):
    athlete_df = df.drop_duplicates(subset=['Name',"Region"])
    male = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    female = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = male.merge(female, on='Year')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0,inplace=True)
    return final



