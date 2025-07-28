import os
from kasa import Discover, Credentials

from logger import logger


# raised when the plug initialization fails
class PlugInitError(Exception):
    pass


async def plug_init():
    logger.info(f"Initializing plug")
    try:
        creds = Credentials(os.getenv("EMAIL"), os.getenv("PASSWORD"))
        devices = await Discover.discover(credentials=creds)

        # find target device by MAC
        for ip, device in devices.items():
            await device.update()
            if device.mac.lower() != os.getenv("PLUG_MAC").lower():
                logger.debug(f"Skipping device with IP {ip}, MAC {device.mac} and alias {device.alias}")
                continue

            logger.info("Plug initialized successfully")
            return device

        raise PlugInitError(f"Device with MAC {os.getenv('PLUG_MAC')} not found")

    except PlugInitError:
        raise

    except Exception as e:
        logger.critical(f"Failed to create Plug instance: {str(e)}", exc_info=True)
        raise PlugInitError("Failed to create Plug instance") from e
