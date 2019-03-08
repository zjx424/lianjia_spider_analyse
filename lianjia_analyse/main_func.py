from lianjia_analyse.calculate import area1_df,unit_df,total_df,table,total_table,expensive_unit_info,expensive_total_info,string_mean
from lianjia_analyse.make_plot import make_bar_plot,bar_stack_plot,show_normal_info

'''展示基本信息,需要添加的是极差,以及其他可以反应房价高低的数据信息'''
show_normal_info(y=0,s=65,text=string_mean)
show_normal_info(y=0,s=5,text=expensive_unit_info)
show_normal_info(y=0,s=5,text=expensive_total_info)
make_bar_plot(title='区域二手房数量条形图',color='SkyBlue',x = area1_df.index.tolist(),y = area1_df.url.tolist(),xlabel='区域',ylabel='二手房数量')
make_bar_plot(title='区域二手房单价条形图',color='SkyBlue',x = unit_df.index.tolist(),y = unit_df.values.tolist(),xlabel='区域',ylabel='单价(单位 元/平方米)')
make_bar_plot(title='区域二手房总价条形图',color='SkyBlue',x = total_df.index.tolist(),y = total_df.values.tolist(),xlabel='区域',ylabel='总价(单位 万元)')
bar_stack_plot(title='商品房区域单价分布',table=table,xlabel='区域',ylabel='单价(单位:元/平方米)')
bar_stack_plot(title='商品房区域总价分布',table=total_table,xlabel='区域',ylabel='总价(单位(万元))')



