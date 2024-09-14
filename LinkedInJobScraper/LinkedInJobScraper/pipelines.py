# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import mysql.connector
from dotenv import load_dotenv
import os


class LinkedinjobscraperPipeline:
    def process_item(self, item, spider):
        adapter=ItemAdapter(item)
        fieldNames=adapter.field_names();
        for field_name in fieldNames:
            if(adapter[field_name]!=None):
                adapter[field_name] = re.sub(r'<[^>]+>', '', adapter.get(field_name))
                adapter[field_name] = re.sub(r'\n', '', adapter[field_name])
                if(field_name!="job_description"):
                    adapter[field_name]=adapter[field_name].strip()
               
        return item
class saveToDatabase:
    load_dotenv(dotenv_path='.sensitive')
    def __init__(self):
        self.conn=mysql.connector.connect(
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('PASS')
        )
