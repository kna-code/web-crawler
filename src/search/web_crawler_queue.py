import queue;
import threading;

class WebCrawlerQueue:
    lock = threading.Lock()
    queue = queue.Queue()
    url_set = { "" }

    def enqueue(self, url: str):
        sanitized_url = url.strip().lower()

        with self.lock:
            if not(sanitized_url in self.url_set):
                self.url_set.add(sanitized_url)
                self.queue.put(sanitized_url)

    def dequeue(self):
        with self.lock:
            try:
                return self.queue.get()
            except:
                return None

    def size(self):
        return self.queue.size()
    
    def empty(self):
        return self.queue.empty()