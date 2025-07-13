from PyP100 import PyP100
import os

from ip_finder import find_ip_by_mac
from logger import logger


# raised when the plug initialization fails
class PlugInitError(Exception):
    pass


def plug_init():
    logger.info(f"Initializing plug")
    try:
        # find plug ip address
        plug_ip = find_ip_by_mac(os.getenv('PLUG_MAC'))
        if plug_ip is None:
            raise PlugInitError("Could not find plug IP")

        # create plug object
        plug = PyP100.P100(plug_ip, os.getenv("EMAIL"), os.getenv("PASSWORD"))

        logger.info("Plug initialized successfully")
        return plug
    except Exception as e:
        logger.critical(f"Failed to create Plug instance: {str(e)}", exc_info=True)
        raise PlugInitError("Failed to create Plug instance") from e
