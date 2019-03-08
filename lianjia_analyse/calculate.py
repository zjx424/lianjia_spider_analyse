import pandas as pd
import math
import re
from lianjia_analyse.read_data import get_df



# df = get_df()
'''
对数据进行处理,去重,取商品房的
'''
df = pd.read_csv('./csvfiles/dg.csv')

df.drop_duplicates(inplace=True)
data = df[df['type'] == '商品房']

len_data=len(data)
total_price_mean = round(data.total_price.mean(), 2)
unit_price_mean = round(data.unit_Price.mean(), 2)
area_mean=round(data['area'].apply(lambda x:float(x[:-2])).mean(),2)

string_total_price_mean="该地区的平均总价为:{}  万元\n".format(total_price_mean)
string_unit_price_mean="该地区的平均单价为:{}  元/平方米\n".format(unit_price_mean)
string_area_mean="该地区的平均面积为:{}  平方米".format(area_mean)
string_mean=string_total_price_mean+string_unit_price_mean+string_area_mean


area1_df = data.groupby(by="area1").count()
area1_df = area1_df.sort_values(by='url', ascending=False)
rate = round(area1_df.url/len_data, 3)
area1_df = area1_df.assign(rate=rate)
area1_df = area1_df[['url', 'rate']]
area1_df = area1_df[area1_df.rate > 0.01]
sum_area1_df = sum(area1_df.url)
new_rate = round(area1_df.url/sum_area1_df, 3)
area1_df=area1_df.assign(rate=new_rate)


area1_list=area1_df.index.tolist()

'''寻找可以替代的方法,tabel???'''
concat_list=[]

for area1 in area1_list:
    concat_list.append(data[data['area1']==area1])
    needed_df=pd.concat(concat_list)
'''needed_df用于之后对总价,单价的统计'''



'''单价总价平均值条形图'''
unit_df_values=[]
total_df_values=[]
unit_dict={}
total_dict={}
for area1 in area1_list:
    re_df=data[data['area1']==area1]
    unit_df_values.append(round(re_df['unit_Price'].mean(),1))
    total_df_values.append(round(re_df['total_price'].mean(),1))
for i,j in zip(area1_list,unit_df_values):
    unit_dict[i]=j
unit_df=pd.Series(unit_dict)
unit_df.sort_values(ascending=False,inplace=True)

for i,j in zip(area1_list,total_df_values):
    total_dict[i] = j
total_df=pd.Series(total_dict)
total_df.sort_values(ascending=False,inplace=True)
'''单价总价平均值条形图'''


'''单价堆叠图'''
max_unit=needed_df.unit_Price.max()/10000
min_unit=needed_df.unit_Price.min()/10000
top=math.ceil(max_unit)
low=math.floor(min_unit)
droped_data=needed_df.assign(unit_price=needed_df.unit_Price/10000)
bins=[]
for i in range(low,top+1):
    bins.append(i)

if len(bins)<10:
    bins=[i*10000 for i in bins]
    bins_data=pd.cut(droped_data.unit_Price,bins=bins)
    table=droped_data.pivot_table('unit_Price',index='area1',columns=bins_data,aggfunc='count')
else:
    bins_data=pd.cut(droped_data.unit_price,bins=bins).value_counts()
    re_bins=[]
    bins_data=bins_data/bins_data.sum()
    bins_data=bins_data[bins_data>0.01]
    strlist=[]
    for i in bins_data.index.tolist():
        i=str(i)
        strlist.append(i)
    re_list=[]
    for i in strlist:
        j=re.findall('(\d+)',i)[0]
        re_list.append(j)
    for i in re_list:
        i=int(i)
        re_bins.append(i)
    re_bins=sorted(re_bins)
    re_bins=[i*10000 for i in re_bins]
    bins_data=pd.cut(droped_data.unit_Price,bins=re_bins)
    table=droped_data.pivot_table('unit_Price',index='area1',columns=bins_data,aggfunc='count')
'''单价堆叠图'''



'''总价堆叠图'''
max_total=needed_df.total_price.max()/100
min_total=needed_df.total_price.min()/100
top=math.ceil(max_total)
low=math.floor(min_total)
droped_data=needed_df.assign(total_Price=needed_df.total_price/100)
total_bins=[]
for i in range(low,top+1):
    total_bins.append(i)
bins_data=pd.cut(droped_data.total_Price,bins=total_bins).value_counts()
dict_cut = {'cut':bins_data.index,'numbers':bins_data.values}
df_cut = pd.DataFrame(dict_cut)
df_cut=df_cut.assign(rate=df_cut.numbers/bins_data.sum())
df_cut=df_cut[df_cut.rate>0.01]
strlist=[]
for i in df_cut.cut.tolist():
    i=str(i)
    strlist.append(i)
re_list=[]
for i in strlist:
    j=re.findall('(\d+)',i)[0]
    re_list.append(j)
re_list=[int(i) for i in re_list]
re_list.sort()
re_list=[i*100 for i in re_list]
bins_data=pd.cut(droped_data.total_price,bins=re_list)
total_table=droped_data.pivot_table('total_price',index='area1',columns=bins_data,aggfunc='count')

'''总价堆叠图'''

'''单价前十贵address'''
expensive_list=needed_df.sort_values(by='unit_Price',ascending=False)
df_expensive=expensive_list[['address','unit_Price','total_price']]
df_expensive_top10=df_expensive.drop_duplicates(subset='address').head(10)
df_expensive_top10.index=range(1,11)

head = '    商品房单价前十的小区\n\n排名   名称         单价     总价     \n'
expensive_unit_info = ''
for i, j in zip(df_expensive_top10.values, range(1, 11)):
    address = i[0].replace(' ', '')
    string_to_use = str(j) + '    ' + address + '    ' + str(i[1]) + '    ' + str(i[2]) + '\n'
    expensive_unit_info += string_to_use
expensive_unit_info = head + expensive_unit_info
'''单价前十贵address'''

'''总价前十贵address'''
expensive_list=needed_df.sort_values(by='total_price',ascending=False)
df_expensive=expensive_list[['address','unit_Price','total_price']]
df_expensive_top10=df_expensive.drop_duplicates(subset='address').head(10)
df_expensive_top10.index=range(1,11)

head = '    商品房总价前十的小区\n\n排名   名称         单价     总价     \n'
expensive_total_info = ''
for i, j in zip(df_expensive_top10.values, range(1, 11)):
    address = i[0].replace(' ', '')
    string_to_use = str(j) + '    ' + address + '    ' + str(i[1]) + '    ' + str(i[2]) + '\n'
    expensive_total_info += string_to_use
expensive_total_info = head + expensive_total_info
'''总价前十贵address'''