"""Fill HTTP tracker with random dummy data.

- Simulate HTTP request / responses texts

- Data does not make sense, but give you some interactivity

- Used to test TUI responsiveness
"""
import datetime
import random
import time
from threading import Thread

from top.redis.tracker import RedisTracker
from top.web.task import HTTPTask


tracker = RedisTracker.create_default_instance(HTTPTask)


task_counter = 0


def event_generator():
    global task_counter

    min_next_delay = 0.01
    max_next_delay = 1
    min_req_duration = 0
    max_req_duration = 5
    methods = ["GET", "POST", "PUT"]
    paths = ["/", "/api/register", "/api/login", "/about", "/contact"]
    client_ips = ["123.123.123.123"]
    response_codes = [200, 301, 404]

    next_event = datetime.datetime.utcnow()

    while True:
        # Sleep until the next event
        now = datetime.datetime.utcnow()
        left = (next_event - now).total_seconds()
        if left > 0:
            time.sleep(left)

        t = HTTPTask.create_from_current_thread(
            task_counter,
            method=random.choice(methods),
            path=random.choice(paths),
            request_headers={
                "Client-addr": random.choice(client_ips)
            }
        )

        task_counter += 1

        # Add some GET params
        if t.method == "GET":
            t.params = {}
            if random.random() > 0.5:
                t.params["next-page"] = "aaa"

            if random.random() > 0.5:
                t.params["previous-page"] = "bbb"

        tracker.start_task(t)
        print(t)

        # Request "being processed"
        time.sleep(random.uniform(min_req_duration, max_req_duration))

        t.response_status_code = random.choice(response_codes)
        t.response_headers = {
            "Content-length": random.randint(0, 1000),
        }

        tracker.end_task(t)
        print(t)

        next_event = datetime.datetime.utcnow() + datetime.timedelta(seconds=random.uniform(min_next_delay, max_next_delay))


def main():
    tracker.clear()
    generator_threads = 20
    for i in range(generator_threads):
        thread = Thread(target=event_generator)
        thread.start()

    time.sleep(9999)


if __name__ == "__main__":
    main()