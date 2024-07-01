from locust import FastHttpUser, tag, task

from api_helper import rand_fund_transfer_request


def custom_wait_time_function(locust):
    wait_time = locust.environment.parsed_options.wait_time
    return float(wait_time)


def is_legit_error(err_msg):
    return (
        "Insufficient funds in debit account" in err_msg
        or "Invalid debit or credit account" in err_msg
    )


def call_fund_transfer_api(client):
    payload = rand_fund_transfer_request()
    with client.post(
        url="/api/casa/transfers",
        headers={"content-type": "application/json"},
        json=payload,
        catch_response=True,
    ) as response:
        if response.status_code == 201:
            response.success()
        elif response.status_code == 422 and is_legit_error(response.text):
            print("business erorr, considered success")
            response.success()
        else:
            print(f"{response.status_code},{response.text}")
            print(payload)
            response.failure(response.text)


class PythonApiUser(FastHttpUser):
    host = "http://localhost:5000"
    wait_time = custom_wait_time_function

    @task
    @tag("python_fund_transfer")
    def call_fund_transfer_api(self):
        call_fund_transfer_api(self.client)


class JavaApiUser(FastHttpUser):
    host = "http://localhost:8080"
    wait_time = custom_wait_time_function

    @task
    @tag("java_fund_transfer")
    def call_fund_transfer_api(self):
        call_fund_transfer_api(self.client)
