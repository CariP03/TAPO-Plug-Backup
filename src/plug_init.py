from PyP100 import PyP100
import os

from ip_finder import find_ip_by_mac


def plug_init():
    # find plug ip address
    plug_ip = find_ip_by_mac(os.getenv('PLUG_MAC'))

    # create plug object
    return PyP100.P100(plug_ip, os.getenv("EMAIL"), os.getenv("PASSWORD"))