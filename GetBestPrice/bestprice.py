from ast import Index
from bs4 import BeautifulSoup
import requests
import pandas as pd

title=[]
link=[]
reviews=[]
rating=[]
discountedprice=[]
originalprice=[]
deliverystatus=[]

searchproduct=input('Enter your Product:')

url='https://www.amazon.in/s?k='+str(searchproduct.replace(' ','+'))
print(url)
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.96 Safari/537.36'
    }

def getdata(url):
    try:
        response=requests.get(url,headers=headers)
        soup=BeautifulSoup(response.text,'html.parser')
        return soup
    except: 
        return "401"

def parsehtml(soup):
    if(soup!="401"):
        itemlist=soup.find_all('div',{'data-component-type':'s-search-result'})
        for products in itemlist:
            title.append(products.find('span',{'class':'a-size-medium a-color-base a-text-normal'}).text)
            link.append("https://www.amazon.in/"+str(products.find('a',{'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']))
            try:
                reviews.append(products.find('span',{'class':'a-size-base'}).text)
            except:
                reviews.append(str('None'))
            try:
                rating.append(products.find('div',{'class':'a-row a-size-small'}).find('span').text)
            except:
                rating.append(0)
            discountedprice.append(products.find('span',{'class':'a-price'}).find('span').text)
            originalprice.append(products.find('span',{'class':'a-price a-text-price'}).find('span').text)
            try:
                deliverystatus.append(products.find('span',{'aria-label':'FREE Delivery by Amazon'}).text)
            except:
                deliverystatus.append(str('None'))
    else:
        return "No data"

def getnextpage(soup):
    try:
        nextpage=soup.find('div',{'class':'a-section a-text-center s-pagination-container'}).find('a')['href']
        url='https://www.amazon.in/'+str(nextpage)
    except:
        url='None'
    return url


while True:
    soup=getdata(url)
    parsehtml(soup)
    url=getnextpage(soup)
    if url=='None':
        break

df=pd.DataFrame({'ProductName':title,'Link':link,'Reviews':reviews,'Rating':rating,'DiscountedPrice':discountedprice,'OriginalPrice':originalprice,'Delivery':deliverystatus})
df.to_csv('Bestprice.csv',index=False)
