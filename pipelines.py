# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime

from itemadapter import ItemAdapter
from twisted.enterprise import adbapi

class MysqlPipeline(object):

        @classmethod
        def from_crawler(cls, crawler):
            # 从项目的配置文件中读取相应的参数
            # cls.MYSQL_DB_NAME = crawler.settings.get("MYSQL_DB_NAME")
            cls.HOST = crawler.settings.get("MYSQL_HOST")
            cls.PORT = crawler.settings.get("MYSQL_PORT")
            cls.USER = crawler.settings.get("MYSQL_USER")
            cls.PASSWD = crawler.settings.get("MYSQL_PASSWORD")
            return cls()

        def open_spider(self, spider):
            self.dbpool = adbapi.ConnectionPool('pymysql', host=self.HOST, port=self.PORT, user=self.USER,
                                                passwd=self.PASSWD, charset='utf8mb4')

        def process_item(self, item, spider):
            # 提交
            self.dbpool.runInteraction(self.insert_db, item)
            return item

        def handle_error(self, failure):
            # 处理异步插入时的异常
            print(failure)

        def close_spider(self, spider):
            # 关闭连接
            self.dbpool.close()

        def insert_db(self, cur, item):
            # 取出数据，执行cur sql
            values = (
                item['shop_name'],
                item['title'],
                item['price']
            )
            sql = 'INSERT INTO ruigang.guangzhoudazhong VALUES (%s,%s,%s)'
            cur.execute(sql, values)

