import time

class Repeater:

    def __init__(self):
        self.task = None
        self.repeat_interval = 0
        self.curent_time = 0
        self.last_reset = time.time()

    def set_repeat_interval_in_seconds(self, seconds: int):
        self.repeat_interval = seconds

    def set_task(self, task):
        self.task = task

    def non_blocking_repeat(self):
        if time.time() - self.last_reset >= self.repeat_interval:
            self.task()
            self.last_reset = time.time()
