from .search_request import SearchRequest 
from .search_result import SearchResult
from .search_result import SearchResultExcerpt
from .search_result_queue import SearchResultQueue
from .web_crawler_queue import WebCrawlerQueue
from .search_utils import SearchUtils
from enum import Enum
import queue
import threading
import time
import httplib2
import logging

class WebCrawlerWorker:
    status = Enum('WebCrawelerWorkerStatus', ['None', 'Processing', 'Waiting', 'Stopping'])
    thread: threading.Thread
    id: int
    search_request: SearchRequest
    search_queue: WebCrawlerQueue
    result_queue: SearchResultQueue

    def __init__(self, id: str, search_request: SearchRequest, search_queue: WebCrawlerQueue, result_queue: SearchResultQueue):
        self.id = id
        self.search_request = search_request
        self.search_queue = search_queue
        self.result_queue = result_queue
        self.status = 'None'

    def set_status(self, status):
        self.status = status
        logging.info(f'WebCrawlerWorker[{self.id}]: set_status: {status}')

    def start_thread(self):
        if self.status == 'None':
            self.thread = threading.Thread(target=self.work_loop)
            self.thread.start()
            self.set_status('Processing')
        else:
            logging.error(f'WebCrawlerWorker[{self.id}]: Worker thread status is {self.status}')


    def stop_thread(self):
        if self.status == 'Processing' or self.status == 'Waiting':
            self.status = 'Stopping'
            self.thread.join() # wait for the thread finish
            self.set_status('None')

    def active(self):
        return self.status == 'Processing' or self.status == 'Stopping'

    def work_loop(self):
        while True:
            if self.status == 'Stopping':
                break # Stop was requsted
            else:
                url = self.search_queue.dequeue()
                if url:

                    self.set_status('Processing')
                    self.process_url(url)
                else:
                    self.set_status('Waiting')
                    time.sleep(1)

    def process_url(self, url):
        logging.info(f'WebCrawlerWorker[{self.id}]: Processing {url}')
        try:

            # Query the URL
            resp, contents = httplib2.Http().request(url)
            str_contents = contents.decode('utf-8')

            # Handle any results
            result = SearchUtils.search_keywords(self.search_request, url, str_contents)
            logging.info(f'WebCrawlerWorker[{self.id}]: Processing {url}, Match={result is not None}')
            if result:
                self.result_queue.enqueue(result)

            # Handle any links
            links = SearchUtils.search_links(self.search_request, str_contents)
            logging.info(f'WebCrawlerWorker[{self.id}]: Processing {url}, # Links={len(links)}')
            for link in links:
                logging.debug(f'WebCrawlerWorker[{self.id}]: Processing {url}, Link={link}')
                self.search_queue.enqueue(link)   
        except Exception as Argument:
            logging.exception(f'WebCrawlerWorker[{self.id}]: Processing {url}, Exception{Argument}')
   