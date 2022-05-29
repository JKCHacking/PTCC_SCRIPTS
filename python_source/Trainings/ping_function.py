#!usr/bin/env python

import platform
import subprocess

def ping(host):
    if platform.system().lower() == "windows":
        param = "-n"
    else:
        param = "-c"

    command = ["ping", param, '4', host]
    return subprocess.call(command)

if __name__ == "__main__":
    host = "www.google.com"
    retcode = ping(host)

    print(retcode)

    if retcode:
        print("Successfully PINGED {}".format(host))
    else:
        print("Unsuccessfully PINGED {}".format(host))
