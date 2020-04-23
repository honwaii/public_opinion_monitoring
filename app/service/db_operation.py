import pymysql
import pprint
from app.util.cfg_operator import config


def get_conn():
    host = config.get_config('host')
    user = config.get_config('user')
    password = config.get_config('password')
    database = config.get_config('database')
    return pymysql.connect(host=host, user=user, password=password, database=database, charset='utf8')


def query_data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()


def query_data_with_param(sql, param):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, param)
        return cursor.fetchall()
    finally:
        conn.close()


def insert_or_update_data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        ret = cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()
    return ret


# 新增blob数据，避免sql注入问题
def insert_with_param(sql, param):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        # 成功自动返回1
        ret = cursor.execute(sql, param)
        conn.commit()
        if ret == 1:
            print("insert successfully.")
            cursor.execute("select LAST_INSERT_ID()")
            return cursor.fetchall()
        else:
            return 0
    finally:
        conn.close()


if __name__ == '__main__':
    sql = "insert into pom_user (user_name,password) values (%s, %s)"
    sql = "select * from pom_user"
    # data = insert_with_param(sql, ('root', '12345678'))
    data = query_data(sql)
    pprint.pprint(data)
