from locust import HttpUser, events, run_single_user, task

from api_tasks import rand_fund_transfer_request


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--wait-time", type=str, dest="wait_time", default="1", help="wait time between requests")
    parser.add_argument("--data", type=str, dest="data_file", default="seed.csv", help="csv file for load generation")


@events.test_start.add_listener
def _(environment, **kw):
    print(f"Custom argument supplied: {environment.parsed_options.wait_time}")


def custom_wait_time_function(locust):
    wait_time = locust.environment.parsed_options.wait_time
    return float(wait_time)


def custom_data_file_function(locust):
    data_file = locust.environment.parsed_options.data_file
    return data_file


class FundTransferApiUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = custom_wait_time_function
    data_file = custom_data_file_function

    @task
    def call_fund_transfer_api(self):
        response = self.client.post(
            url="/api/casa/transfers",
            headers={"content-type": "application/json"},
            json=rand_fund_transfer_request(self.data_file),
        )
        if response.status_code != 201:
            print(response.text)


if __name__ == "__main__":
    run_single_user(FundTransferApiUser)
