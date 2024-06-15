from locust import HttpUser, events, run_single_user, task

from api_tasks import rand_fund_transfer_request


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--wait-time", type=str, dest="wait_time", default="1", help="wait time between requests")


@events.test_start.add_listener
def _(environment, **kw):
    print(f"Custom argument supplied: {environment.parsed_options.wait_time}")


def custom_wait_time_function(locust):
    wait_time = locust.environment.parsed_options.wait_time
    return float(wait_time)


class FundTransferApiUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = custom_wait_time_function

    @task
    def call_fund_transfer_api(self):
        response = self.client.post(
            url="/api/casa/transfers",
            headers={"content-type": "application/json"},
            json=rand_fund_transfer_request("t1m.csv"),
        )
        if response.status_code != 201:
            print(response.text)


if __name__ == "__main__":
    run_single_user(FundTransferApiUser)
