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

class WebCrawlerWorker:
    status = Enum('WebCrawelerWorkerStatus', ['None', 'Processing', 'Waiting', 'Stopping'])
    thread: threading.Thread
    search_request: SearchRequest
    search_queue: WebCrawlerQueue
    result_queue: SearchResultQueue

    def __init__(self, id: str, search_request: SearchRequest, search_queue: WebCrawlerQueue, result_queue: SearchResultQueue):
        self.search_request = search_request
        self.search_queue = search_queue
        self.result_queue = result_queue
        self.status = 'None'


    def start_thread(self):
        if self.status == 'None':
            self.thread = threading.Thread(target=self.work_loop)
            self.thread.start()
            self.status = 'Processing'
        else:
            logging.error(f'Worker thread status is {self.status}')


    def stop_thread(self):
        if self.status == 'Processing' or self.status == 'Waiting':
            self.status = 'Stopping'
            self.thread.join() # wait for the thread finish
            self.status = 'None'

    def active(self):
        return self.status == 'Processing' or self.status == 'Stopping'

    def work_loop(self):
        while True:
            if self.status == 'Stopping':
                break # Stop was requsted
            else:
                self.status = 'Processing'
                url = self.search_queue.enqueue()
                if url:
                    self.process_url(url)
                else:
                    self.status = 'Waiting'
                    time.sleep(1)

    def process_url(self, url):
        # Query the URL
        resp, contents = httplib2.Http().request(url)
        str_contents = contents.decode('utf-8')

        # Handle any results
        result = SearchUtils.search_keywords(self.search_request, url, str_contents)
        if result:
            self.result_queue.enqueue(result)

        # Handle any links
        links = SearchUtils.search_links(self.search_request, str_contents)
        for link in links:
            self.search_queue.enqueue(link)   

   