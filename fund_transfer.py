from locust import FastHttpUser, tag, task

from api_helper import rand_fund_transfer_request


def custom_wait_time_function(locust):
    wait_time = locust.environment.parsed_options.wait_time
    return float(wait_time)


class PythonApiUser(FastHttpUser):
    host = "http://localhost:5000"
    wait_time = custom_wait_time_function

    @task
    @tag("python_fund_transfer")
    def call_fund_transfer_api(self):
        payload = rand_fund_transfer_request()
        response = self.client.post(
            url="/api/casa/transfers",
            headers={"content-type": "application/json"},
            json=payload,
        )
        if response.status_code != 201:
            print(response.text)


class JavaApiUser(FastHttpUser):
    host = "http://localhost:8080"
    wait_time = custom_wait_time_function

    @task
    @tag("java_fund_transfer")
    def call_fund_transfer_api(self):
        global all_accounts
        payload = rand_fund_transfer_request()
        response = self.client.post(
            url="/spring/api/casa/transfers",
            headers={"content-type": "application/json"},
            json=payload,
        )
        if response.status_code != 201:
            print(response.text)
