from collections import deque
import threading

class SimpleQueue:
    def __init__(self):
        self.q = deque()
        self.lock = threading.Lock()

    def push(self, item):
        with self.lock:
            self.q.append(item)

    def pop(self):
        with self.lock:
            if self.q:
                return self.q.popleft()
        return None

    def size(self):
        with self.lock:
            return len(self.q)
