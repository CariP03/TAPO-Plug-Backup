import sys
import time
from dotenv import load_dotenv

import host_commands as host
from backup import execute_backup, BackupError
from logger import logger, start_logging
from plug_init import PlugInitError

load_dotenv()  # load variables


if __name__ == '__main__':
    start_logging()

    was_online = True
    try:
        # check host status and turn it on if offline
        host.init_host()

        if not host.is_online():
            was_online = False
            host.turn_on()

            time.sleep(90)  # waiting for host startup

        # backup
        execute_backup("cloud")
        execute_backup("images")

    except BackupError as e:
        logger.critical("Aborting: backup process failed", exc_info=True)
        sys.exit(1)

    except PlugInitError as e:
        logger.critical("Startup failed: plug not initialized", exc_info=True)
        sys.exit(1)

    except Exception as e:
        logger.critical("Unexpected fatal error", exc_info=True)
        sys.exit(1)

    finally:
        # turn off the remote host
        if not was_online:
            host.turn_off()

