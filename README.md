# HTTP Request Sender

This program allows you to make HTTP requests to a specified URL and provides statistics on the performance of the requests.

## Usage

To use the program, follow these steps:

1. Clone the repository or download the source code.
2. Open a terminal or command prompt and navigate to the directory where the program is located.
3. Run the `install.py` file to install the dependencies and create the `ccload` load command.
4. Run the program using the following command:
    ```
    ccload -u <url> -n <number_requests> -c <number_concurrent>
    ```
    Replace `<url>` with the URL you want to make requests to. `<number_requests>` and `<number_concurrent>` are optional parameters that specify the number of requests to make and the number of concurrent requests, respectively. If not provided, the default values are 10 requests and 1 concurrent request.
5. The program will make the specified number of requests to the URL and display the following statistics:
    - Total Requests (2XX): The total number of successful requests with a status code of 200.
    - Failed Requests (5XX): The total number of failed requests with a status code of 500 or higher.
    - Requests per second: The average number of requests made per second.
    - Total Request Time (s) (Min, Max, Mean): The minimum, maximum, and average time taken for each request.
    - Time to First Byte (s) (Min, Max, Mean): The minimum, maximum, and average time taken from sending the request to receiving the first byte of the response.
    - Time to Last Byte (s) (Min, Max, Mean): The minimum, maximum, and average time taken from sending the request to receiving the last byte of the response.

## Example

To make 20 requests to the URL "https://example.com" with 5 concurrent requests, run the following command:
    ```
    ccload -u https://example.com -n 20 -c 5
    ```

I created this program was designed based on a challenge on the "Coding Challenges" website: https://codingchallenges.fyi/challenges/challenge-load-tester