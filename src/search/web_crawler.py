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
from datetime import datetime
import os
import logging
import re

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

    lastStatusUpdateTime = 0

    def __init__(self, search_request: SearchRequest, output_dir: str):
        self.search_request = search_request
        self.output_dir = output_dir

    def run(self):

        startTime = time.perf_counter()
        print(f'{self.search_request.name} - Starting')

        self.initialize_result_files()
        self.search_queue.enqueue(self.search_request.start_url)

        self.log_progress()
        self.start_workers()
        while self.any_worker_active() or (not self.search_queue.empty()) or (not self.result_queue.empty()):

            self.log_progress()

            # Process the results queue
            result = self.result_queue.dequeue()
            if result:
                self.process_result(result)
            else:  
                time.sleep(1)

        self.stop_workers()
        self.log_progress()

        endTime = time.perf_counter()
        
        # Pretty-print the time.
        totalSeconds = endTime-startTime
        hours = totalSeconds%(60*60)
        minutes = totalSeconds%(60*60)
        seconds = totalSeconds - hours*60*60 - minutes*60

        timeLog = f'{self.search_request.name} - Completed in {hours} hours, {minutes}, {totalSeconds - seconds}'
        logging.info(timeLog)
        print(timeLog)

    def log_progress(self):
        # Log based on the interval
        currentTime = time.perf_counter()
        if currentTime - self.lastStatusUpdateTime > self.statusFrequencySeconds:
            self.lastStatusUpdateTime = currentTime
            print(f'{self.search_request.name}: Matches Found: {self.result_count}, Pages Processed: {self.search_queue.deque_count}, Queue Size: {self.search_queue.size()}, Active Worker Threads: {self.active_worker_count()}')
    

    def start_workers(self):
        for i in range(0, self.workerCount):
            worker = WebCrawlerWorker(i+1, self.search_request, self.search_queue, self.result_queue)
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
    
    def active_worker_count(self):
        count = 0
        for worker in self.workers:
            if worker.active():
                count = count + 1
       
        return count
    
    def initialize_result_files(self):

        # Ensure the output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)     

        if self.search_request.debug_output_enabled and not os.path.exists(self.search_request.debug_output_dir):
            os.makedirs(self.search_request.debug_output_dir)  

        # Create the file name
        search_name = self.search_request.name.lower()
        search_name = search_name.replace(" ", "_")

        # Logging
        self.output_log_file = f'{self.output_dir}/{search_name}_log.txt'
        logging.basicConfig(filename=self.output_log_file, 
                            filemode='a',
                            format="%(levelname)s: %(message)s", 
                            level=logging.DEBUG,
                            force=True
        )

        # Report - Detailed
        self.output_report_detailed_file = f'{self.output_dir}/{search_name}_report_detailed.csv'
        logging.info(f"Output File Report Detailed: {self.output_report_detailed_file}")
        file = open(self.output_report_detailed_file, "w")
        try:
            file.write(f'Name, Keyword, URL, Location, Excerpt\n')
        finally:
            file.close()

        # Report - Detailed
        self.output_report_summary_file = f'{self.output_dir}/{search_name}_report_summary.csv'
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
                escaped_text = re.escape(excerpt.text)
                file.write(f'{result.name},{result.keyword},{result.url},{excerpt.location},"{escaped_text}\n"')
        finally:
            file.close()

        # Report - Summary
        file = open(self.output_report_summary_file, "a")
        try:
            file.write(f'{result.name},{result.keyword},{result.url},{len(result.excerpts)}\n')
        finally:
            file.close()
        

        self.result_count = self.result_count + 1

