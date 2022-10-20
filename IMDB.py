'''Lets scarap data from IMDB website using Beautifulsoup libary'''

from bs4 import BeautifulSoup
import requests
import re

data=requests.get('https://www.imdb.com/title/tt0110912/?ref_=nv_sr_srsg_0')
response=data.content
response=BeautifulSoup(response,'html.parser')
#print(response.a.prettify())
#cast = response.find(name='div', attrs={'data-testid':'shoveler-items-container','class':"ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--wraps-at-above-l ipc-shoveler__grid"})
cast_data=response.find_all(name='a',attrs={'data-testid':'title-cast-item__actor','class':'sc-bfec09a1-1 gfeYgX'})


for cast_d in cast_data:
    
    data=cast_d.prettify()
    #print(data)
    Actor_Actress=cast_d.text
    link=cast_d.get('href')
    data_link='https://www.imdb.com'+link

    res=requests.get(data_link)
    res=res.content
    movie=BeautifulSoup(res,'html.parser')
    # movie_name=[]
    # movie_data=movie.findAll(name='a',attrs={'class':"knownfor-ellipsis"})
    # for movie_d in movie_data:
    #     #movie_name=movie_d.text
    #     movie_name+=movie_d.text
    #     print(movie_name)
     
    movie_data=movie.findAll(name='a',attrs={'class':"knownfor-ellipsis"})
    for movie_d in movie_data:
        # movie={}
        # movie_name=movie_d.text
        # movie['title']=movie_d.text
        # print(movie)
        
        movie_name=movie_d.text
        print(movie_name)
    
    movie_year=movie.findAll(name='div', attrs={'class':'knownfor-year'})
    #movie_year=movie.findAll(name='span',attrs={'class':"knownfor-ellipsis"})
    for movie_y in movie_year:
        year=movie_y.text
        print(year)
    #movies=movie_data
   
    #print(movies)
    #print(movie)
    
    Data={
       'name':Actor_Actress,
       'link':data_link,
       'Movie':[{
        'Title':movie_name,
        'Year':year
       }]
      
    }
    
    print(Data)