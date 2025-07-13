import time
from dotenv import load_dotenv

import pc_commands as pc
from backup import execute_backup

load_dotenv()  # load variables


if __name__ == '__main__':
    # check PC status and turn it on if offline
    was_online = True
    if not pc.is_online():
        was_online = False
        pc.turn_on()

        time.sleep(90)  # waiting for PC startup

    # backup
    execute_backup("cloud")
    execute_backup("images")

    # turn off the PC
    if not was_online:
        pc.turn_off()
