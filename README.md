# lianjia_spider_analyse

爬虫部分:
利用python的scrapy框架对链家(lianjia.com)进行爬取,爬取城市约95个,每个城市二手房数量约20000条,数据总数约为200万条.

分析部分:
利用numpy,pandas对抓取到的数据进行普通的分析,如平均值,极值,区域平均值.

可视化部分:
在jupyternotebook上利用matplotlib对数据进行可视化,显示出堆叠图,条形图,饼状图.

功能:用户可以输入想要查看的城市,从数据库中读取到该城市的二手房数据,读取出csv文件(或者excel可供用户选择)保存在本地,等待用户自己进行分析,或者使用分析部分,直接帮助用户对数据进行分析.直接显示出统计数据,条形图,堆叠图等可视化信息,以供用户进行大致的了解


下面是广州部分数据的展示:

包括:标题(title),网页地址(url),地址(address),每平方米单价(unit_Price),总价(total_price),面积(area),区域(area1),朝向(direction),层数(floor),房间结构(rooms),类型(type),推荐原因(recommended)
![阿里云mysql数据库](https://github.com/zjx424/lianjia_spider_analyse/blob/master/%E9%93%BE%E5%AE%B6github/%E6%95%B0%E6%8D%AE%E5%B1%95%E7%A4%BA.png)

可视化(以广州为准):
![均值](https://github.com/zjx424/lianjia_spider_analyse/blob/master/%E9%93%BE%E5%AE%B6github/%E5%9D%87%E5%80%BC.png)
![昂贵](https://github.com/zjx424/lianjia_spider_analyse/blob/master/%E9%93%BE%E5%AE%B6github/%E6%98%82%E8%B4%B5.png)
![区域数量条形图](https://github.com/zjx424/lianjia_spider_analyse/blob/master/%E9%93%BE%E5%AE%B6github/%E6%95%B0%E9%87%8F%E6%9D%A1%E5%BD%A2%E5%9B%BE.png)
![单价条形图](https://github.com/zjx424/lianjia_spider_analyse/blob/master/%E9%93%BE%E5%AE%B6github/%E5%8D%95%E4%BB%B7%E6%9D%A1%E5%BD%A2%E5%9B%BE.png)
![总价条形图](https://github.com/zjx424/lianjia_spider_analyse/blob/master/%E9%93%BE%E5%AE%B6github/%E6%80%BB%E4%BB%B7%E6%9D%A1%E5%BD%A2%E5%9B%BE.png)
![单价堆叠图](https://github.com/zjx424/lianjia_spider_analyse/blob/master/%E9%93%BE%E5%AE%B6github/%E5%8D%95%E4%BB%B7%E5%88%86%E5%B8%83.png)
![总价堆叠图](https://github.com/zjx424/lianjia_spider_analyse/blob/master/%E9%93%BE%E5%AE%B6github/%E6%80%BB%E4%BB%B7%E5%88%86%E5%B8%83.png)
