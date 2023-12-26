import argparse
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import time
import requests


class RequestSender:
    def __init__(self, url):
        self.url = url

    def send_request(self):
        raise NotImplementedError


class HTTPRequestSender(RequestSender):
    def send_request(self):
        response = requests.get(self.url)
        return response


class StatisticsCalculator:
    def __init__(self):
        self.successes = Counter()
        self.failures = Counter()
        self.total_times = []
        self.first_byte_times = []
        self.last_byte_times = []
        self.response_codes = Counter()

    def calculate_statistics(self, responses):
        for response in responses:
            total_time = response["end_time"] - response["start_time"]
            self.total_times.append(total_time)

            first_byte_time = response["response"].elapsed.total_seconds()
            self.first_byte_times.append(first_byte_time)

            last_byte_time = total_time - first_byte_time
            self.last_byte_times.append(last_byte_time)

            self.response_codes.update([response["response"].status_code])

            if response["response"].status_code == 200:
                self.successes.update([1])
            else:
                self.failures.update([1])

    def print_summary(self):
        total_requests = self.successes[1] + self.failures[1]
        failed_requests = self.failures[1]
        requests_per_second = total_requests / sum(self.total_times)

        min_total_time = min(self.total_times)
        max_total_time = max(self.total_times)
        mean_total_time = sum(self.total_times) / len(self.total_times)

        min_first_byte_time = min(self.first_byte_times)
        max_first_byte_time = max(self.first_byte_times)
        mean_first_byte_time = sum(self.first_byte_times) / len(self.first_byte_times)

        min_last_byte_time = min(self.last_byte_times)
        max_last_byte_time = max(self.last_byte_times)
        mean_last_byte_time = sum(self.last_byte_times) / len(self.last_byte_times)

        print("Results:")
        print(f"Total Requests (2XX).......................: {total_requests}")
        print(f"Failed Requests (5XX)......................: {failed_requests}")
        print(f"Request/second.............................: {requests_per_second:.2f}\n")
        print("Total Request Time (s) (Min, Max, Mean).....: {:.2f}, {:.2f}, {:.2f}".format(min_total_time, max_total_time, mean_total_time))
        print("Time to First Byte (s) (Min, Max, Mean).....: {:.2f}, {:.2f}, {:.2f}".format(min_first_byte_time, max_first_byte_time, mean_first_byte_time))
        print("Time to Last Byte (s) (Min, Max, Mean)......: {:.2f}, {:.2f}, {:.2f}".format(min_last_byte_time, max_last_byte_time, mean_last_byte_time))


def make_request(url, number_requests=10, number_concurrent=1):
    successes = Counter()
    failures = Counter()
    response_data = []

    request_sender = HTTPRequestSender(url)

    with ThreadPoolExecutor(max_workers=number_concurrent) as executor:
        def send_request(_):
            try:
                start_time = time.time()
                response = request_sender.send_request()
                end_time = time.time()

                response_data.append({
                    "start_time": start_time,
                    "end_time": end_time,
                    "response": response
                })

                if response.status_code == 200:
                    successes.update([1])
                else:
                    failures.update([1])
            except requests.RequestException:
                failures.update([1])

        executor.map(send_request, range(number_requests))

    statistics_calculator = StatisticsCalculator()
    statistics_calculator.calculate_statistics(response_data)
    statistics_calculator.print_summary()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make HTTP requests")
    parser.add_argument("-u", "--url", help="The URL to make a request to", required=True)
    parser.add_argument("-n", "--number_requests", help="Number of requests to make", default=10)
    parser.add_argument("-c", "--number_concurrent", help="Number of concurrent requests", default=1)

    args = parser.parse_args()

    url = args.url
    number_requests = int(args.number_requests)
    number_concurrent = int(args.number_concurrent)

    make_request(url, number_requests, number_concurrent)
