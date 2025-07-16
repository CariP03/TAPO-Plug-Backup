from dotenv import load_dotenv

load_dotenv()  # load variables

import sys

import host_commands as host
from backup import cycle_backups, BackupError
from logger import logger
from plug_init import PlugInitError

if __name__ == '__main__':
    was_online = True
    try:
        was_online = host.start_host()
        cycle_backups()

    except BackupError as e:
        logger.critical("Aborting: backup process failed", exc_info=True)
        sys.exit(1)

    except PlugInitError as e:
        logger.critical("Startup failed: plug not initialized", exc_info=True)
        sys.exit(1)

    except FileNotFoundError as e:
        logger.critical("Script directory not found", exc_info=True)
        sys.exit(1)

    except Exception as e:
        logger.critical("Unexpected fatal error", exc_info=True)
        sys.exit(1)

    finally:
        # turn off the remote host
        if not was_online:
            host.turn_off()
