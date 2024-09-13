import scrapy

from LinkedInJobScraper.items import jobItem

class LinkedinspiderSpider(scrapy.Spider):
    name = "linkedInSpider"
    allowed_domains = ["www.linkedin.com","ro.linkedin.com"]
    start_urls = [f"https://www.linkedin.com/jobs/search?keywords=Data%20Engineer&location=Romania&geoId=106670623&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum={i}" for i in range(0, 250, 25)]
    def parse(self, response):
        linkuri=response.xpath("//a[@class='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]']/@href").getall()
        for job_link in linkuri:
            yield response.follow(job_link, callback=self.parse_job_page)

    def parse_job_page(self,response):
        job=jobItem()
        detaliiJob=response.xpath("//span[@class='description__job-criteria-text description__job-criteria-text--criteria']/text()").getall()
        job['job_url']=response.url
        job['job_title']=response.xpath("//h1[@class='top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title']/text()").get() #trebe curatat de \n
        job['job_company']=response.xpath("//a[@class='topcard__org-name-link topcard__flavor--black-link']/text()").get()  #trebe curatat de \n
        job['job_nr_candidates']=response.xpath("//figcaption[@class='num-applicants__caption']/text()").get() #trebe curatat de \n
        job['job_description']=response.xpath("//div[@class='description__text description__text--rich']").get() #trebe curatat de \n si de <> </>
        if(len(detaliiJob)==4):
            job['job_level']=detaliiJob[0]
            job['job_program']=detaliiJob[1]
            job['job_category']=detaliiJob[2]
            job['job_activity_sector']=detaliiJob[3]
        else:
            job['job_level']="none"
            job['job_program']="none"
            job['job_category']="none"
            job['job_activity_sector']="none"
        yield job


    
