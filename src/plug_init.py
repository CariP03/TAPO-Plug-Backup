from PyP100 import PyP100
from dotenv import load_dotenv
import os

from ip_finder import find_ip_by_mac

load_dotenv()  # load variables


def plug_init():
    # find plug ip address
    plug_ip = find_ip_by_mac(os.getenv('PLUG_MAC'))

    # create plug object
    return PyP100.P100(plug_ip, os.getenv("EMAIL"), os.getenv("PASSWORD"))