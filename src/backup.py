import subprocess
from dotenv import load_dotenv
import os
from pathlib import Path

from ip_finder import find_ip_by_mac

load_dotenv()  # load variables

def execute_backup():
    # build BORG_REPO dynamically
    host = find_ip_by_mac(os.getenv('PC_MAC'))
    username = os.getenv('SSH_USERNAME')
    path = os.getenv('BORG_PATH')

    os.environ["BORG_REPO"] = f"ssh://{username}@{host}:{path}"

    # execute backup
    script_path = Path(__file__).resolve().parent / "backup.sh"
    subprocess.run([script_path], check=True)


