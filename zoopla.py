from bs4 import BeautifulSoup
import requests

data=requests.get('https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&view_type=list')
response=data.content
response=BeautifulSoup(response,'html.parser')
#print(response.prettify)
details=response.find_all(name='div',attrs={'data-testid':"regular-listings"})
# img=response.find_all("img", class_="c-iIvYAS")
img=response.find_all("img")
print(len(img))
for im in img:
    print(im.get('src'))


