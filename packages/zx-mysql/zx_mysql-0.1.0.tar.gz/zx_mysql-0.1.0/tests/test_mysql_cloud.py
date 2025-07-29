import os
from mysql_cloud import MySqlCloud


DEFAULT_HOST = '120.48.151.191'
DEFAULT_PORT = 3306
DEFAULT_USER = 'zxtech'
DEFAULT_PASSWORD = os.getenv('SUPER_PASSWORD')

# 修正：添加必要的初始化参数
test = MySqlCloud(DEFAULT_HOST, DEFAULT_PORT, DEFAULT_USER, DEFAULT_PASSWORD)

def test_query():
    # 建立数据库连接，假设数据库名为 'your_database_name'，请根据实际情况修改
    database_name = 'requirement'
    connection = test.connect_database(database_name)
    result = []
    if connection:
        # 修改查询语句，添加 LIMIT 100
        query = "SELECT custom_name, title, sub_system FROM requirement LIMIT 100"
        rows = test.execute_query(query)
        if rows:
            print("查询结果:")
            for row in rows:
                print(row)
            result = rows
        else:
            print("未查询到数据。")
    else:
        print("数据库连接失败，请检查配置信息。")
    return result


def create_test_database():
    """创建 test 数据库"""
    database_name = 'test'
    if test.create_database(database_name):
        print(f"成功创建数据库 {database_name}")
    else:
        print(f"创建数据库 {database_name} 失败")

def create_test_table():
    """在 test 数据库中创建表"""
    database_name = 'test'
    table_name = 'test_table'
    # 修改表结构，使其与查询字段同步
    table_schema = "custom_name VARCHAR(255), title VARCHAR(255), sub_system VARCHAR(255)"
    if test.create_table(database_name, table_name, table_schema):
        print(f"成功在 {database_name} 中创建表 {table_name}")
    else:
        print(f"在 {database_name} 中创建表 {table_name} 失败")

def insert_test_data():
    """向 test_table 表中插入来自 test_query 的数据"""
    database_name = 'test'
    table_name = 'test_table'
    insert_query = f"INSERT INTO {table_name} (custom_name, title, sub_system) VALUES (%s, %s, %s)"
    data_rows = test_query()
    connection = test.connect_database(database_name)
    if connection and data_rows:
        for data in data_rows:
            test.execute_insert(insert_query, data)
        print(f"成功向 {table_name} 插入 {len(data_rows)} 条数据")
    else:
        if not connection:
            print(f"连接数据库 {database_name} 失败，无法插入数据")
        else:
            print("没有可插入的数据。")

def test_execute_sql():
    # 连接到数据库
    database_name = 'test'
    if test.connect_database(database_name):
        try:
            # 使用 test 数据库
            use_db_sql = "USE test"
            result = test.execute_sql(use_db_sql)
            if result:
                print("成功使用 test 数据库")
            else:
                print("使用 test 数据库失败")

            # 删除 test_table 表中的所有数据
            delete_sql = "DELETE FROM test_table"
            result = test.execute_sql(delete_sql)
            if result:
                print("成功删除 test_table 表中的所有数据")
            else:
                print("删除 test_table 表数据失败")
        except Exception as e:
            print(f"执行 SQL 语句时出错: {e}")
        finally:
            # 关闭数据库连接
            test.close_connection()
    else:
        print(f"无法连接到数据库 {database_name}")

if __name__ == "__main__":
    #test_query()
    #test_database_test()
    test_execute_sql()