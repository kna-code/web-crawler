import queue;
import threading;

from .search_result import SearchResult

class SearchResultQueue:
    lock = threading.Lock()
    queue = queue.Queue()

    def enqueue(self, search_result: SearchResult):

        with self.lock:
            queue.put(search_result)

    def dequeue(self):
        with self.lock:
            try:
                return self.queue.get()
            except:
                return None;

    def size(self):
        return self.queue.size()
    
    def empty(self):
        return self.queue.empty()