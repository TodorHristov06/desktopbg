# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
from jsonschema import validate, ValidationError
from desktop_bg.schemas import computer_schema

class SQLitePipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect('computers.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS computers (
                id INTEGER PRIMARY KEY,
                processor TEXT,
                gpu TEXT,
                motherboard TEXT,
                ram TEXT,
                UNIQUE(processor, gpu, motherboard, ram)
            )
        ''')

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            validate(instance=item, schema=computer_schema)
        except ValidationError as e:
            spider.logger.error(f'Validation error: {e.message}')
            return item

        self.cursor.execute('''
            INSERT OR IGNORE INTO computers (processor, gpu, motherboard, ram) VALUES (?, ?, ?, ?)
        ''', (item['processor'], item['gpu'], item['motherboard'], item['ram']))
        return item
