import subprocess
import os
from pathlib import Path

from ip_finder import find_ip_by_mac


def execute_backup(repo_name):
    # build BORG_REPO dynamically
    host = find_ip_by_mac(os.getenv('PC_MAC'))
    username = os.getenv('SSH_USERNAME')
    full_path = os.path.join(os.getenv('BASE_REPOS_PATH'), repo_name)

    os.environ["BORG_REPO"] = f"ssh://{username}@{host}:{full_path}"

    # execute backup
    script_path = Path(__file__).resolve().parent / "backup.sh"
    subprocess.run([script_path], check=True, env=os.environ)


