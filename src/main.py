from dotenv import load_dotenv

load_dotenv()  # load variables

import sys
import os
import time
from pathlib import Path

import host_commands as host
from backup import execute_backup, BackupError
from logger import logger
from plug_init import PlugInitError

if __name__ == '__main__':
    was_online = True
    try:
        # check host status and turn it on if offline
        host.init_host()

        if not host.is_online():
            was_online = False
            host.turn_on()

            logger.info("Waiting for host to come online...")
            time.sleep(90)  # waiting for host startup

        # cycle through scripts directory to execute all backups
        BASE_DIR = Path(__file__).resolve().parent  # /app/src
        script_dir = BASE_DIR.parent / "scripts"  # /app/scripts
        if not script_dir.is_dir():
            raise FileNotFoundError("Script directory not found")

        for sh_file in script_dir.glob("*.sh"):
            logger.debug(f"Retrieved script {sh_file}")
            execute_backup(sh_file)

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
