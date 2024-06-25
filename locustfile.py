import sys

from locust import events, run_single_user

from fund_transfer import JavaApiUser, PythonApiUser


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--wait-time", type=str, dest="wait_time", default="1", help="wait time between requests")


@events.test_start.add_listener
def _(environment, **kw):
    print(f"Custom argument supplied: {environment.parsed_options.wait_time}")


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "python":
        run_single_user(PythonApiUser)
    elif sys.argv[1] == "java":
        run_single_user(JavaApiUser)
    else:
        print("Usage: locustfile.py [python|java]")
        sys.exit(1)
