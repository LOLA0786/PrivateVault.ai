import json
import time
import uuid

class EventStore:

    def __init__(self, file_path="pv_events.log"):
        self.file_path = file_path

    def append_event(self, event_type, payload):
        event = {
            "id": str(uuid.uuid4()),
            "type": event_type,
            "payload": payload,
            "timestamp": time.time()
        }

        with open(self.file_path, "a") as f:
            f.write(json.dumps(event) + "\n")

        return event

    def replay(self):
        events = []
        try:
            with open(self.file_path, "r") as f:
                for line in f:
                    events.append(json.loads(line.strip()))
        except FileNotFoundError:
            pass
        return events
