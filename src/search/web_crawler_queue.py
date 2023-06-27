import queue;
import threading;

class WebCrawlerQueue:
    lock = threading.Lock()
    queue = queue.Queue()
    url_set = { "" }
    enque_count = 0
    deque_count = 0

    def enqueue(self, url: str):
        sanitized_url = url.strip().lower()

        with self.lock:
            if not(sanitized_url in self.url_set):
                self.url_set.add(sanitized_url)
                self.queue.put(sanitized_url)
                self.enque_count = self.enque_count + 1

    def dequeue(self):
        with self.lock:
            try:
                value = self.queue.get(False, 0.1)
                self.deque_count = self.deque_count + 1
                return value
            except:
                return None

    def size(self):
        return self.queue.qsize()
    
    def empty(self):
        return self.queue.empty()