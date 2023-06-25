from .search_request import SearchRequest 
from .search_result import SearchResult
from .search_result import SearchResultExcerpt
from .search_result_queue import SearchResultQueue
from .web_crawler_queue import WebCrawlerQueue
from .web_crawler_worker import WebCrawlerWorker
from .search_utils import SearchUtils
from enum import Enum
import queue
import threading
import time
import httplib2
import datetime

class WebCrawler:
    search_request: SearchRequest
    output_dir: str
    output_log_file: str
    output_report_detailed_file: str
    output_report_summary_file: str

    workerCount = 7
    statusFrequencySeconds = 10
    workers = []
    search_queue = WebCrawlerQueue()
    result_queue = SearchResultQueue()
    result_count = 0

    def __init__(self, search_request: SearchRequest, output_dir: str):
        self.search_request = search_request
        self.output_dir = output_dir

    def run(self):

        self.search_queue.enqueue(self.search_request.start_url)

        self.start_workers()

        lastStatusUpdateTime = time.perf_counter()

        while self.any_worker_active() or not self.search_queue.empty() or not self.result_queue.empty():

            # Print the status Size periodially
            currentTime = time.perf_counter()
            if currentTime - lastStatusUpdateTime > self.statusFrequencySeconds:
                lastStatusUpdateTime = currentTime
                print(f'{self.search_request.name}: Matching Urls: {self.result_count}, Queue Size: {self.search_queue.size()}')

            # Process the results queue
            result = self.result_queue.dequeue()
            if result:
                self.process_result(result)
            else:  
                time.sleep(1)

        self.stop_workers()


    def start_workers(self):
        for i in range(0, self.workerCount):
            worker = WebCrawlerWorker(i+1, self.search_request, self.search_queue, self.result_queue)
            print(f'worker type = {type(worker)}')
            worker.start_thread()
            self.workers.append(worker)
        
    def stop_workers(self):
        for worker in self.workers:
            worker.stop_thread()

        self.workers.clear()

    def any_worker_active(self):
        for worker in self.workers:
            if worker.active():
                return True
        return False
    
    def initialize_result_files(self):

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        dir = self.output_dir + "/" + timestamp

        # Ensure the output directory exists
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)     

        # Logging
        self.output_log_file = f'{dir}/log_{timestamp}.txt'
        logging.basicConfig(filename=self.outputFileLog, 
                            filemode='a',
                            format="%(levelname)s: %(message)s", 
                            level=logging.DEBUG,
                            force=True
        )

        # Report - Detailed
        self.output_report_detailed_file = f'{dir}/report_detailed_{timestamp}.txt'
        logging.info(f"Output File Report Detailed: {self.output_report_detailed_file}")
        file = open(self.output_report_detailed_file, "w")
        try:
            file.write(f'Name, Keyword, URL, Location, Excerpt\n')
        finally:
            file.close()

        # Report - Detailed
        self.output_report_summary_file = f'{dir}/report_detailed_{timestamp}.txt'
        logging.info(f"Output File Report Summary: {self.output_report_summary_file}")
        file = open(self.output_report_summary_file, "w")
        try:
            file.write(f'Name, Keyword, URL, Count\n')
        finally:
            file.close()


    def process_result(self, result: SearchResult):

        # Report - Detailed
        file = open(self.output_report_detailed_file, "a")
        try:
            #file.write(f'Name, Keyword, URL, Location, Excerpt\n')
            for excerpt in result.excerpts:
                file.write(result.name, result.keyword, result.url, excerpt.location, excerpt.exceprt)
        finally:
            file.close()

        # Report - Summary
        file = open(self.output_report_summary_file, "a")
        try:
            file.write(result.name, result.keyword, result.url, len(result.excerpts))
        finally:
            file.close()
        

        self.result_count = self.result_count + 1