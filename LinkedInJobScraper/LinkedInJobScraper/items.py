import scrapy

class jobItem(scrapy.Item):
    job_url = scrapy.Field()
    job_title = scrapy.Field()
    job_company = scrapy.Field()
    job_nr_candidates = scrapy.Field()
    job_description = scrapy.Field()
    job_level = scrapy.Field()
    job_program = scrapy.Field()
    job_category = scrapy.Field()
    job_activity_sector = scrapy.Field()
