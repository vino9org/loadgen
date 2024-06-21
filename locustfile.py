from locust import FastHttpUser, events, run_single_user

from api_tasks import rand_fund_transfer_request, read_accounts_from_csv


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


class PythonApiUser(FastHttpUser):
    host = "http://localhost"
    wait_time = custom_wait_time_function

    def on_start(self):
        data_file = self.environment.parsed_options.data_file
        self.all_accounts = read_accounts_from_csv(data_file)

    def call_fund_transfer_api(self):
        payload = rand_fund_transfer_request(self.all_accounts)
        response = self.client.post(
            url="/fastapi/api/casa/transfers",
            headers={"content-type": "application/json"},
            json=payload,
        )
        if response.status_code != 201:
            print(response.text)


class JavaApiUser(FastHttpUser):
    host = "http://localhost"
    wait_time = custom_wait_time_function

    def on_start(self):
        data_file = self.environment.parsed_options.data_file
        self.all_accounts = read_accounts_from_csv(data_file)

    def call_fund_transfer_api(self):
        payload = rand_fund_transfer_request(self.all_accounts)
        response = self.client.post(
            url="/spring/api/casa/transfers",
            headers={"content-type": "application/json"},
            json=payload,
        )
        if response.status_code != 201:
            print(response.text)


if __name__ == "__main__":
    run_single_user(PythonApiUser)
