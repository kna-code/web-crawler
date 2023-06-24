#!/usr/bin/env python
#
# To use:
# > python3 web_crawler.py 

from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess
import csv
from datetime import datetime
import os
import re
import logging

class KeyWordSpider(scrapy.Spider):
    name = "abortion_search"
    keyword = "abortion"
    inputFile = "./data/schools.csv"
    outputDir = "./output/"
    outputFileReport = None
    outputFileLog = None

    def start_requests(self):

        # Configure Output Path
        if not os.path.exists(self.outputDir):
            os.makedirs(self.outputDir)     

        self.outputFileReport = "./output/report_" +  datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
        self.outputFileLog = "./output/report_" +  datetime.now().strftime("%Y%m%d%H%M%S") + ".log"

        # Configure logging
        logging.basicConfig(filename=self.outputFileLog, 
                            filemode='a',
                            format="%(levelname)s: %(message)s", 
                            level=logging.DEBUG,
                            force=True
        )

        # Parse Input
        if not os.path.isfile(self.inputFile):
            logging.error(f'Input File Not Found: {self.inputFile}')


        logging.info(f"Output File Report:{self.outputFileReport}")

        with open(self.inputFile , newline='\n') as csvfile:
            inputFileReader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(inputFileReader) # skip the header
            for row in inputFileReader:
                if(len(row) == 3):
                    school = row[0]
                    domain = row[1]
                    startingUrl = row[2]

                    print(', '.join(row))
                    request = scrapy.Request(url=startingUrl, callback=self.parse)
                    request.cb_kwargs['school'] = school
                    request.cb_kwargs['domain'] = domain
                    yield request
                else:
                    logging.error("Invalid Row: " + ', '.join(row))


    def parse(self, response, school, domain):

        logging.info(f'Parsing {response.url}')
        
        # Log the keywords on this page
        file = open(self.outputFileReport, "w")
        try:
            searchResults = response.xpath("//*[contains(text(), '{keyword}')]").getall()
            for searchResult in searchResults:
                url = response.url
                text = searchResult

                file.write('"{label}","{url}","{text}"')
        finally:
            file.close()

        # Look for links to follow
        links = response.xpath('//div/p/a')
        numLinks = len(links)
        logging.info(f'LINKS: {numLinks}')
        for link in links:
            if re.search(rootUrl, link, re.IGNORECASE):
                    request2 = scrapy.Request(url=url, callback=self.parse)
                    request2.cb_kwargs['school'] = school
                    request2.cb_kwargs['domain'] = domain
                    yield request2



def main():


    # Start the Crawler
    settings = {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    }
    process = CrawlerProcess(settings)
    process.crawl(KeyWordSpider)
    process.start()

if __name__ == "__main__":
    main()

