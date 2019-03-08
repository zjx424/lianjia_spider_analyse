from lxml import etree
import requests
url="https://www.lianjia.com/city/"
response=requests.get(url)


html=etree.HTML(response.text)
city_url=html.xpath('//div[@class="city_recommend"]//li/a/@href')
city_url.remove('https://bj.lianjia.com/')
urllist=[]
for url in city_url:
    urllist.append(url+"ershoufang/rs/")

all_url=[]
for i in urllist:
    if '.fang' not in i:
        all_url.append(i)
