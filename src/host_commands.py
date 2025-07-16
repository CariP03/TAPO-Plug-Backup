import subprocess
import os
import time

from plug_init import plug_init, PlugInitError
from ip_finder import get_host_ip
from logger import logger

plug = None


def __init_host():
    global plug
    try:
        plug = plug_init()
    except PlugInitError as e:
        raise


# function that turn on the pc by turning off the plug and then turning it on
def __turn_on():
    logger.info("Turning on remote host")
    try:
        plug.turnOff()
        plug.turnOn()
    except Exception as e:
        logger.critical(f"Error turning on plug: {e}", exc_info=True)
        raise


# check host status and turn it on if offline
def start_host():
    __init_host()

    was_online = True
    if not is_online():
        was_online = False
        __turn_on()

        logger.info("Waiting for host to come online...")
        time.sleep(90)  # waiting for host startup

    return was_online


def __shutdown_host(host):
    # soft shutdown
    logger.info("Attempting graceful shutdown via SSH")
    try:
        subprocess.run(["ssh", f"{os.getenv('SSH_USERNAME')}@{host}", "sudo shutdown -h now"], check=True)
        logger.info("Waiting for host to shutdown...")
        time.sleep(45)
        logger.info("Remote host turned off successfully")
    except subprocess.CalledProcessError as e:
        logger.error(
            f"Failed to shut down host via SSH. Proceeding to turn off plug without graceful shutdown: {e}",
            exc_info=True)


def turn_off():
    logger.info("Turning off remote host")
    host = get_host_ip()
    if host is not None:
        __shutdown_host(host)
    else:
        logger.warning(f"Failed to find host IP. Proceeding to turn off plug without graceful shutdown")

    try:
        plug.turnOff()
        logger.info("Plug turned off successfully")
    except Exception as e:
        logger.error(f"Failed to turn off plug: {e}", exc_info=True)


def is_online(count=4, timeout=2):
    logger.info("Checking if remote host is online")
    host = get_host_ip()
    if host is not None:

        # Windows systems
        # cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]

        # Linux systems
        cmd = ["ping", "-c", str(count), "-W", str(timeout), host]

        try:
            result = subprocess.run(cmd,
                                    check=True,
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)
            logger.info("Remote host is online")
            return True

        except subprocess.CalledProcessError as e:
            logger.warning(f"Ping failed: host is unreachable ({host})")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during ping: {e}", exc_info=True)
            return False

    logger.info("Remote host is offline (IP not found)")
    return False
