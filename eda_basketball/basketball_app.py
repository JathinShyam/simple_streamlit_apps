import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple websccraping of NBA player stats Data
* **Python libraries:** base64, pandas, streamlit
* **Data Source: ** [Basketball-reference.com](https://www.basketball-reference.com/).

""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1960,2022))))

@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age=='Age'].index) #Deleting repeating headers in content
    raw= raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

#sidebar Team Selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

#Sidebar Position Selection
unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
selected_pos = st.sidebar.multiselect("Position", unique_pos, unique_pos)

#Filtering
st.write(playerstats)
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]
st.write(playerstats.Tm.isin(selected_team))
st.write(df_selected_team)

#Download NBA player data as csv
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

#Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header("Intercorrelation Matrix Heatmap")
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f,ax = plt.subplots(figsize =(7,5))
        #st.set_option('deprecation.showPyplotGlobalUse', False)
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot()
