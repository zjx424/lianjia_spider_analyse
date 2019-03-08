import pandas as pd
from sqlalchemy import create_engine



def get_df():
    table_name = input('input tabel_name:')
    '''想办法将账户密码IP地址隐藏'''
    engine = create_engine('mysql+pymysql://root:456765xx@120.77.39.227:3306/lianjia')

    sq='select * from %s'%table_name
    sql=sq+';'
    # read_sql_query的两个参数: sql语句， 数据库连接
    df = pd.read_sql_query(sql, engine)

    path='./csvfiles/%s.csv'%table_name
    df.to_csv(path)#保存成相应table_name名的csv文件

    df=pd.read_csv(path)
    return df
if __name__ == '__main__':
    get_df()
