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
from mysql.connector import Error


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
    load_dotenv(dotenv_path="C:\\Users\\Andrei\\Desktop\\Portofoliu\\LinkedInJobScraper&data\\.sensitive")
    def __init__(self):
        self.conn=mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASS")      
        )
        self.cur=self.conn.cursor()
        try:
            self.cur.execute("Create database if not exists Jobs")
        except Error as e:
            print(f"Some error occurred:{e}")
        finally:
            self.conn.database="Jobs"
        self.cur.execute("""
        create table if not exists Jobs(
        job_id int NOT NULL auto_increment,
        job_url varchar(255),
        job_title varchar(255),
        job_company varchar(255),
        job_nr_candidates varchar(255),
        job_description varchar(7000),
        job_level varchar(255),
        job_program varchar(255),
        job_category varchar(255),
        job_activity_sector varchar(255),
        primary key(job_id)
        )
                         """)
    def process_item(self,item,spider):     
        self.cur.execute("""
        insert into Jobs(job_url,job_title,job_company,job_nr_candidates,job_description,job_level,job_program,job_category,job_activity_sector)
                         values( %s,%s,%s,%s,%s,%s,%s,%s,%s)
                         """,(
                             item["job_url"],
                             item["job_title"],
                             item["job_company"],
                             item["job_nr_candidates"],
                             item["job_description"],
                             item["job_level"],
                             item["job_program"],
                             item["job_category"],
                             item["job_activity_sector"],
                         ))
        self.conn.commit()
        return item  
    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()          



