import sched
import time

def hello():
    print("Hello world!")

scheduler = sched.scheduler(time.time, time.sleep)

def repeat_task():
    scheduler.enter(5, 1, hello, ())
    scheduler.enter(5, 1, repeat_task, ())

repeat_task()
while True:
    scheduler.run(blocking=False)