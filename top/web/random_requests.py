"""Generate random HTTP requests to localhost.

To have some traffic on our web-top screen.
"""
import datetime
import random
import time
from threading import Thread

import requests

server = "http://localhost:8080"


def event_generator():
    global task_counter

    min_next_delay = 0.01
    max_next_delay = 1
    methods = ["GET", "POST", "PUT"]
    paths = ["/", "/api/register", "/api/login", "/about", "/contact"]
    countries = ["FI", "US", "T1", "CH", "GI"]

    next_event = datetime.datetime.utcnow()

    session = requests.Session()

    while True:
        # Sleep until the next event
        now = datetime.datetime.utcnow()
        left = (next_event - now).total_seconds()
        if left > 0:
            time.sleep(left)

        method = random.choice(methods)
        path = random.choice(paths)

        # Add some GET params
        params = None
        if method == "GET":
            params = {}
            if random.random() > 0.5:
                params["next-page"] = "aaa"

            if random.random() > 0.5:
                params["previous-page"] = "bbb"

        # Some requests have geolocation
        headers = {}
        if random.random() > 0.05:
            headers["CF-IPCountry"] = random.choice(countries)

        url = f"{server}{path}"

        req = requests.Request(
            method=method,
            url=url,
            params=params,
            headers=headers,
        )

        req = req.prepare()
        print("Sending request", req.url)

        session.send(req)

        next_event = datetime.datetime.utcnow() + datetime.timedelta(seconds=random.uniform(min_next_delay, max_next_delay))


def main():
    print(f"Generating random HTTP requests to {server}")
    generator_threads = 5
    for i in range(generator_threads):
        thread = Thread(target=event_generator)
        thread.start()

    time.sleep(9999)


if __name__ == "__main__":
    main()
