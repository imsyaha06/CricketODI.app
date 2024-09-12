import streamlit as st
import pandas as pd
import plotly.express as px

# Set up Streamlit page configuration
st.set_page_config(page_title="Cricket Insights", page_icon=":bar_chart:", layout="wide")

# Page title
st.title(":bar_chart: Cricket World Cup Analysis")

# Load data
csv_file = ''
df = pd.read_csv(csv_file)

# Save data to Excel
excel_file = 'originalDataset'
df.to_excel(excel_file, index=False, engine='openpyxl')

# Sidebar for images and filters
st.sidebar.image(r'C:\Users\Rana Comuter\Pictures\ICC.webp')
st.sidebar.header("Please Filter Here:")

# Functions for data analysis
def filter_data(df, team1, team2, ground):
    if team1:
        df = df[df["Team 1"].isin(team1)]
    if team2:
        df = df[df["Team 2"].isin(team2)]
    if ground:
        df = df[df["Ground"].isin(ground)]
    return df

def plot_winner_chart(df):
    if 'Winner' in df.columns:
        winner_counts = df['Winner'].value_counts().reset_index()
        winner_counts.columns = ['Country', 'Count']
        fig = px.bar(winner_counts, x='Country', y='Count', title="<b>Matches won by a Country</b>", color='Country', template="plotly_white")
        st.plotly_chart(fig)
    else:
        st.write("The column 'Winner' does not exist in the DataFrame.")

def plot_margin_chart(df):
    if 'Margin' in df.columns:
        margin_counts = df['Margin'].value_counts().reset_index()
        margin_counts.columns = ['Wickets', 'Count']
        fig = px.bar(margin_counts, x='Count', y='Wickets', color='Wickets', title="<b>Country Won by Margin</b>", orientation='h', template="plotly_white")
        st.plotly_chart(fig)
    else:
        st.write("The column 'Margin' does not exist in the DataFrame.")

def plot_innings_chart(df):
    if 'Innings_Team1' in df.columns and 'Innings_Team2' in df.columns:
        innings_team1 = df['Innings_Team1'].value_counts().reset_index()
        innings_team1.columns = ['Team', 'Count']
        fig1 = px.pie(innings_team1, names='Team', values='Count', hole=0.4, title="<b>Innings Analysis for Team 1</b>", template="plotly_white")
        
        innings_team2 = df['Innings_Team2'].value_counts().reset_index()
        innings_team2.columns = ['Team', 'Count']
        fig2 = px.pie(innings_team2, names='Team', values='Count', hole=0.4, title="<b>Innings Analysis for Team 2</b>", template="plotly_white")
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1)
        with col2:
            st.plotly_chart(fig2)
    else:
        st.write("The columns 'Innings_Team1' or 'Innings_Team2' do not exist in the DataFrame.")

def plot_host_country_chart(df):
    if 'Host_Country' in df.columns:
        host_counts = df['Host_Country'].value_counts().reset_index()
        host_counts.columns = ['Host_Country', 'Count']
        fig = px.area(host_counts, x='Host_Country', y='Count', title="<b>Matches Host by a Country</b>", color='Host_Country', template="plotly_white")
        st.plotly_chart(fig)
    else:
        st.write("The column 'Host_Country' does not exist in the DataFrame.")

# Sidebar filters
team1 = st.sidebar.multiselect("Select Your Team:", options=df["Team 1"].unique())
team2 = st.sidebar.multiselect("Select Opposite Team:", options=df["Team 2"].unique())
ground = st.sidebar.multiselect("Select Match Venue:", options=df["Ground"].unique())

# Filter data based on sidebar selections
filtered_df = filter_data(df, team1, team2, ground)

# Check if any filter has been applied
filters_applied = bool(team1) or bool(team2) or bool(ground)

if filters_applied:
    # Display the header if filters are applied
    st.header("Analysis Based on Filters")
    
    # Analysis and plotting based on filtered data
plot_winner_chart(filtered_df)
plot_margin_chart(filtered_df)
plot_innings_chart(filtered_df)
plot_host_country_chart(filtered_df)
