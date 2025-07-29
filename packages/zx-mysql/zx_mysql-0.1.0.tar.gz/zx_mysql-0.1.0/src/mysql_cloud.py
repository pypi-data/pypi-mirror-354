import os
import logging
import pymysql


class MySqlCloud:
    def __init__(self, default_host, default_port, default_user, default_password):
        self.host = default_host
        self.port = default_port
        self.user = default_user
        self.password = default_password
        self.connection = None
        self._setup_logging()

    def _setup_logging(self):
        log_dir = ".logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, "mysql_log.txt")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename=log_file
        )
        self.logger = logging.getLogger(__name__)

    def set_config(self, host=None, port=None, user=None, password=None):
        if host:
            self.host = host
        if port:
            try:
                self.port = int(port)
            except ValueError:
                self.logger.error("输入的端口号不是有效的整数。")
        if user:
            self.user = user
        if password:
            self.password = password

    def get_config(self):
        config = {
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password
        }
        log_config = config.copy()
        log_config.pop('password', None)
        self.logger.info("数据库连接信息: %s", log_config)
        return config

    def connect_database(self, database):
        try:
            config = self.get_config()
            log_config = config.copy()
            log_config.pop('password', None)
            self.connection = pymysql.connect(
                host=config["host"],
                port=config["port"],
                user=config['user'],
                password=config['password'],
                database=database
            )
            #print("成功连接到数据库")
            self.logger.info("成功使用配置 %s 连接到数据库: %s", log_config, database)
            return self.connection
        except pymysql.Error as e:
            config = self.get_config()
            log_config = config.copy()
            log_config.pop('password', None)
            print(f"连接数据库出错: {e}")
            self.logger.error("使用配置 %s 连接数据库 %s 出错: %s", log_config, database, e)
            return None

    def execute_query(self, query):
        if not self.connection:
            print("未建立数据库连接，请先连接数据库。")
            self.logger.warning("未建立数据库连接，无法执行查询: %s", query)
            return None
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                self.logger.info("查询执行成功: %s", query)
                return rows
        except pymysql.Error as e:
            print(f"查询执行出错: {e}")
            self.logger.error("查询执行出错: %s，查询语句: %s", e, query)
            return None

    def execute_insert(self, insert_query, data):
        if not self.connection:
            print("未建立数据库连接，请先连接数据库。")
            self.logger.warning("未建立数据库连接，无法执行插入操作: %s", insert_query)
            return
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(insert_query, data)
                self.connection.commit()
                #print("数据插入成功")
                self.logger.info("数据插入成功: %s，数据: %s", insert_query, data)
        except pymysql.Error as e:
            print(f"插入数据出错: {e}")
            self.logger.error("插入数据出错: %s，插入语句: %s，数据: %s", e, insert_query, data)

    def execute_insert_many(self, insert_query, rows):
        if not self.connection:
            print("未建立数据库连接，请先连接数据库。")
            self.logger.warning("未建立数据库连接，无法执行批量插入操作: %s", insert_query)
            return
        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(insert_query, rows)
                self.connection.commit()
                print("数据插入成功")
                self.logger.info("批量数据插入成功: %s，数据行数: %d", insert_query, len(rows))
        except pymysql.Error as e:
            print(f"插入数据出错: {e}")
            self.logger.error("批量插入数据出错: %s，插入语句: %s，数据行数: %d", e, insert_query, len(rows))

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("数据库连接已关闭")
            self.logger.info("数据库连接已关闭")
            self.connection = None


    def create_database(self, database_name):
        """
        创建指定名称的数据库。
        :param database_name: 要创建的数据库名称
        :return: 数据库创建成功返回 True，失败返回 False
        """
        try:
            config = self.get_config()
            log_config = config.copy()
            log_config.pop('password', None)
            # 先不指定数据库连接
            connection = pymysql.connect(
                host=config["host"],
                port=config["port"],
                user=config['user'],
                password=config['password']
            )
            try:
                with connection.cursor() as cursor:
                    query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
                    cursor.execute(query)
                self.logger.info("成功使用配置 %s 创建数据库: %s", log_config, database_name)
                return True
            except pymysql.Error as e:
                self.logger.error("使用配置 %s 创建数据库 %s 出错: %s", log_config, database_name, e)
                return False
            finally:
                connection.close()
        except pymysql.Error as e:
            config = self.get_config()
            log_config = config.copy()
            log_config.pop('password', None)
            print(f"连接数据库出错: {e}")
            self.logger.error("使用配置 %s 连接数据库出错: %s", log_config, e)
            return False

    def create_table(self, database_name, table_name, table_schema):
        """
        在指定数据库中创建表。
        :param database_name: 数据库名称
        :param table_name: 表名称
        :param table_schema: 表的创建语句，例如："id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255)"
        :return: 表创建成功返回 True，失败返回 False
        """
        try:
            # 连接到指定数据库
            if not self.connect_database(database_name):
                self.logger.error("无法连接到数据库 %s，无法创建表 %s", database_name, table_name)
                return False

            try:
                create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_schema})"
                result = self.execute_query(create_table_query)
                if result is not None:
                    self.logger.info("成功在数据库 %s 中创建表 %s", database_name, table_name)
                    return True
                else:
                    self.logger.error("在数据库 %s 中创建表 %s 失败", database_name, table_name)
                    return False
            except pymysql.Error as e:
                self.logger.error("在数据库 %s 中创建表 %s 出错: %s", database_name, table_name, e)
                return False
        finally:
            # 关闭数据库连接
            self.close_connection()

    def execute_sql(self, sql, data=None):
        """
        执行任意 SQL 语句。
        :param sql: 要执行的 SQL 语句
        :param data: 可选，用于参数化查询的数据，可为元组、列表等
        :return: 对于查询类语句，返回查询结果；对于写入类语句，执行成功返回 True，失败返回 False
        """
        if not self.connection:
            print("未建立数据库连接，请先连接数据库。")
            self.logger.warning("未建立数据库连接，无法执行 SQL 语句: %s", sql)
            return None if sql.strip().lower().startswith(('select', 'show', 'describe')) else False

        try:
            with self.connection.cursor() as cursor:
                if data:
                    cursor.execute(sql, data)
                else:
                    cursor.execute(sql)

                # 根据 SQL 类型处理结果
                if sql.strip().lower().startswith(('select', 'show', 'describe')):
                    rows = cursor.fetchall()
                    self.logger.info("查询执行成功: %s", sql)
                    return rows
                else:
                    self.connection.commit()
                    self.logger.info("写入操作执行成功: %s", sql)
                    return True
        except pymysql.Error as e:
            print(f"执行 SQL 语句出错: {e}")
            self.logger.error("执行 SQL 语句出错: %s，语句: %s", e, sql)
            if not sql.strip().lower().startswith(('select', 'show', 'describe')):
                self.connection.rollback()
            return None if sql.strip().lower().startswith(('select', 'show', 'describe')) else False
    