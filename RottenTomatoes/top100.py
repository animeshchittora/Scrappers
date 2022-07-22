from bs4 import BeautifulSoup
import requests
from csv import writer
import pandas as pd
rank=[]
name=[]
year=[]
director=[]
adjusted_score=[]

for pages in range(1,6):
    try:
        source=requests.get('https://editorial.rottentomatoes.com/guide/100-best-classic-movies/'+str(pages)+'/')
        soup=BeautifulSoup(source.text,'html.parser')
        movies=soup.find_all('div',class_='row countdown-item')
        moviesindepth=soup.find_all('div',class_='row countdown-item-details')
        for movie in movies:
            rank.append(movie.find('div',class_='countdown-index-resposive').text.strip('#'))
            name.append(movie.find('div',class_='article_movie_title').find('a').text)
            year.append(movie.find('span',class_='subtle start-year').text.strip('(').strip(')'))
        for info in moviesindepth:
            director.append(info.find('div',class_='info director').find('a').text)
            adjusted_score.append(info.find('div',class_='info countdown-adjusted-score').text.strip('Adjusted Score: '))
    except Exception as e:
        print(e)

df=pd.DataFrame({'MovieRank':rank,'Name':name,'ReleaseYear':year,'RTScore':adjusted_score,'Director':director})
df.to_csv('RottenTomatoesTop100.csv',index=False)