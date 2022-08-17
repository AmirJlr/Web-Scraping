import streamlit as st

# create exel file:
import openpyxl

# scrape the data
import requests
from bs4 import BeautifulSoup

# working with data and visulalize
import pandas as pd
import plost
from PIL import Image



### Scrape Data ###

# config exel file
exel = openpyxl.Workbook()
sheet = exel.active
sheet.title = "250 Imdb Movies"
sheet.append(["Rank", "Name", "Year", "Rating"])

# start scraping :
imdb_url =requests.get("https://www.imdb.com/chart/top/") 
soup = BeautifulSoup(imdb_url.text, 'html.parser')

movies = soup.find('tbody',class_ = 'lister-list').find_all('tr')

for movie in movies :
    rank = movie.find('td',class_='titleColumn').text.split('.')[0].strip()
    name = movie.find('td',class_='titleColumn').a.text
    year = movie.find('td',class_='titleColumn').span.text.strip('()')
    rating = movie.find('td',class_='ratingColumn imdbRating').strong.text
    sheet.append([rank,name,year,rating])

#save exel file
#exel.save('TopImdb.csv')

###


# Data

data = pd.read_excel('TopImdb.csv')
print(data.head(5))

# Page setting
st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title('Top 20 Imdb')


# Row A
a1, a2= st.columns((1,9))
a1.image(Image.open('imdb.png'))
a2.metric(" ",' ' , " ")
# a3.metric("Humidity", "86%", "4%")


# Row B
b1, b2, b3 = st.columns(3)
b1.metric(" ", data.Name[0], "1")
b2.metric("Rating :", data.Rating[0], " ")
b3.metric("Year :",  data.Year[0])


st.table(data.head(10)) 

# Row C
c1, c2 = st.columns((6,4))
with c1:
    st.markdown('### Heatmap')
    plost.xy_hist(
    data=data,
    x='Year',
    y='Rating',
    )


    # titanic = sns.load_dataset("titanic")

    # fig = plt.figure(figsize=(10, 4))
    # sns.countplot(x="class", data=titanic)

    # st.pyplot(fig)

with c2:
    st.markdown('### Line chart')
    plost.line_chart(data=data, x='Year', y="Rating")
    # (
    #     data=data,
    #     theta='q2',
    #     color='company')
