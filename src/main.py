from dotenv import load_dotenv

load_dotenv()  # load variables

import sys
import asyncio

import host_commands as host
from backup import cycle_backups, BackupError
from logger import logger
from plug_init import PlugInitError


async def main():
    was_online = None
    try:
        was_online = await host.start_host()
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
            await host.turn_off()

        # close connection with plug
        await host.close_plug()

if __name__ == '__main__':
    asyncio.run(main())