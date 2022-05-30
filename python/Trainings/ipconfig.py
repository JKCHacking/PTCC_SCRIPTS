#!usr/bin/env python

import platform
import subprocess

def check_network_info():
    if platform.system().lower() == "windows":
        command = ["ipconfig", "/all"]
    else:
        command = ["ifconfig"]

    return subprocess.call(command)

if __name__ == "__main__":
    retcode = check_network_info()
    print(retcode)
    
