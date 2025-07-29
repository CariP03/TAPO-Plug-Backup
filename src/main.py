from dotenv import load_dotenv

load_dotenv()  # load variables

import sys
import asyncio

import host_commands as host
from backup import cycle_backups, BackupError
from logger import logger
from plug_init import PlugInitError
from telegram_bot import send_backup_result


async def main():
    was_online = None
    try:
        was_online = await host.start_host()
        return cycle_backups()

    except BackupError as e:
        logger.critical("Aborting: backup process failed", exc_info=True)
        return 2

    except PlugInitError as e:
        logger.critical("Startup failed: plug not initialized", exc_info=True)
        return 2

    except FileNotFoundError as e:
        logger.critical("Script directory not found", exc_info=True)
        return 2

    except Exception as e:
        logger.critical("Unexpected fatal error", exc_info=True)
        return 2

    finally:
        # turn off the remote host
        if not was_online:
            await host.turn_off()

        # close connection with plug
        await host.close_plug()

if __name__ == '__main__':
    exit_code = asyncio.run(main())
    send_backup_result(exit_code)
    sys.exit(exit_code)