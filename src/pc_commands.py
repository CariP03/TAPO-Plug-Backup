import subprocess
import os
import time

from plug_init import plug_init
from ip_finder import find_ip_by_mac

plug = None


def init_pc():
    global plug
    plug = plug_init()


# function that turn on the pc by turning off the plug and then turning it on
def turn_on():
    plug.turnOff()
    plug.turnOn()


def turn_off():
    host = find_ip_by_mac(os.getenv('PC_MAC'))
    if host is not None:
        # soft shutdown
        subprocess.run(["ssh", f"{os.getenv("SSH_USERNAME")}@{host}", "sudo shutdown -h now"], check=True)
        time.sleep(45)

    plug.turnOff()


def is_online(count=4, timeout=2):
    host = find_ip_by_mac(os.getenv('PC_MAC'))
    if host is not None:

        # Windows systems
        # cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]

        # Linux systems
        cmd = ["ping", "-c", str(count), "-W", str(timeout), host]

        result = subprocess.run(cmd,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        return result.returncode == 0

    else:
        return False
