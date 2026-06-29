#!/usr/bin/env python3
import requests
import sys

OK, CORRUPT, MUMBLE, DOWN, CHECKER_ERROR = 101, 102, 103, 104, 110
PORT = 3000
TIMEOUT = 5

def make_request(method, url, data=None):
    try:
        if data is not None:
            r = method(url, json=data, timeout=TIMEOUT)
        else:
            r = method(url, timeout=TIMEOUT)
    except requests.exceptions.Timeout:
        close(DOWN, "Service timeout", "Timeout on {}".format(url))
    except requests.exceptions.ConnectionError:
        close(DOWN, "Service is down", "Connection error to {}".format(url))
    except Exception as ex:
        close(CHECKER_ERROR, "Checker error", "Request failed: {}".format(ex))

    if r.status_code != 200:
        close(MUMBLE, "Invalid HTTP response", "Status code {} from {}".format(r.status_code, url))
    return r

def close(code, public="", private=""):
    if public:
        print(public)
    if private:
        print(private, file=sys.stderr)
    exit(code)

def info(*args):
    close(OK, "vulns: 1")

def check(*args):
    team_ip = args[0]
    url = "http://{}:{}/check".format(team_ip, PORT)
    make_request(requests.get, url)
    close(OK, "Service is OK")

def put(*args):
    # args: [team_ip, flag_id, flag, ...] (может быть больше аргументов)
    team_ip, flag_id, flag = args[0], args[1], args[2]
    url = "http://{}:{}/put".format(team_ip, PORT)
    data = {"flag_id": flag_id, "flag": flag}
    make_request(requests.post, url, data=data)
    print(flag_id)
    close(OK)

def get(*args):
    team_ip, flag_id, flag = args[0], args[1], args[2]
    url = "http://{}:{}/get/{}".format(team_ip, PORT, flag_id)
    r = make_request(requests.get, url)
    received_flag = r.text.strip()
    if received_flag == flag:
        close(OK)
    else:
        close(CORRUPT, "Flag mismatch", "Expected: {}, got: {}".format(flag, received_flag))

def error_arg(*args):
    close(CHECKER_ERROR, private="Wrong command {}".format(sys.argv[1]))

COMMANDS = {
    'check': check,
    'put': put,
    'get': get,
    'info': info
}

if __name__ == '__main__':
    with open("/tmp/checker.log", "a") as f:
        f.write(" ".join(sys.argv) + "\n")
    try:
        COMMANDS.get(sys.argv[1], error_arg)(*sys.argv[2:])
    except Exception as ex:
        close(CHECKER_ERROR, private="INTERNAL ERROR: {}".format(ex))
