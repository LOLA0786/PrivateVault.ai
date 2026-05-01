import heapq
import threading

class PriorityQueue:
    def __init__(self):
        self.q = []
        self.lock = threading.Lock()

    def push(self, priority, item):
        with self.lock:
            heapq.heappush(self.q, (-priority, item))

    def pop(self):
        with self.lock:
            if self.q:
                return heapq.heappop(self.q)[1]
        return None

    def size(self):
        with self.lock:
            return len(self.q)
