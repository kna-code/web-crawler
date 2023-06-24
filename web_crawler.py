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
import re

class KeyWordSpider(scrapy.Spider):
    name = "KeyWordSpider"
    inputFile = "./data/schools.csv"
    outputDir = "./output/"
    outputFileLog = None
    outputFileReport = None

    def start_requests(self):

        # (1) Initiaize the Output Files

        if not os.path.exists(self.outputDir):
            os.makedirs(self.outputDir)     

        # Logging
        self.outputFileLog = "./output/report_" +  datetime.now().strftime("%Y%m%d%H%M%S") + ".log"
        logging.basicConfig(filename=self.outputFileLog, 
                            filemode='a',
                            format="%(levelname)s: %(message)s", 
                            level=logging.DEBUG,
                            force=True
        )

        # Report
        self.outputFileReport = "./output/report_" +  datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
        logging.info(f"Output File Report:{self.outputFileReport}")

        file = open(self.outputFileReport, "w")
        try:
            file.write(f'School,Keyword,URL\n')
        finally:
            file.close()
        

        # (2) Load the Input Files

        # Parse Input
        if not os.path.isfile(self.inputFile):
            logging.error(f'Input File Not Found: {self.inputFile}')

        expectedFormat="School,Domain,Starting URL,Keyword1,Keyword2,Keyword3,..."
        with open(self.inputFile , newline='\n') as csvfile:
            inputFileReader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(inputFileReader) # skip the header            
            line = 1
            for row in inputFileReader:
                line = line+1
                if(len(row) >=4):
                    school = row[0].strip()
                    domain = row[1].strip()
                    startingUrl = row[2]
                    keywords = []
                    for i in range(3, len(row)):
                        # sanitize the input.
                        word = row[i].strip().lower();
                        if(len(word) > 0 ):
                            keywords.append(word)

                    if(len(school) > 0 and len (domain) > 0 and len(startingUrl) > 0 and len(keywords) > 0):
                        request = self.createCrawlRequest(startingUrl, school, domain, keywords)
                        yield request
                    else:
                        logging.error(f'Invalid Row on line {line}: "{",".join(row)}", expected format is "{expectedFormat}"')
                else:
                    logging.error(f'Invalid Row on line {line}: "{",".join(row)}", expected format is "{expectedFormat}"')

    def createCrawlRequest(self, url, school, domain, keywords):
        request = scrapy.Request(url=url, callback=self.parse)
        request.cb_kwargs['school'] = school
        request.cb_kwargs['domain'] = domain
        request.cb_kwargs['keywords'] = keywords
        return request
        


    def parse(self, response, school, domain, keywords):

        logging.info(f'Parsing Domain="{domain}", School="{school}", URL="{response.url}", Keywords="{",".join(keywords)}"')
        
        # Log the keywords on this page
        file = open(self.outputFileReport, "a")
        try:
            # Look for the keyword
            for keyword in keywords:
                if( response.text.find(keyword) >= 0):
                    file.write(f'{school},{keyword},{response.url}\n')
        finally:
            file.close()

        # Look for links
        linkRegExPattern = re.compile('<a href="(\S*)">')        
        for (url) in re.findall(linkRegExPattern, response.text):
            logging.info(f'LINK: {url}')
            request = self.createCrawlRequest(url, school, domain, keywords)
            yield request


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

