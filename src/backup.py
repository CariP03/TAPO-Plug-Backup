import subprocess
import os
from pathlib import Path, PurePosixPath

from ip_finder import find_ip_by_mac
from logger import logger, log_subprocess

# raised when unable to proceed with backup
class BackupError(Exception):
    pass


def execute_backup(repo_name):
    logger.info(f"Executing backup for {repo_name}")
    # build BORG_REPO dynamically
    host = find_ip_by_mac(os.getenv('REMOTE_HOST_MAC'))
    if host is not None:
        username = os.getenv('SSH_USERNAME')
        full_path = PurePosixPath(os.getenv('BORG_REPOS_PATH')) / repo_name
        os.environ['BORG_REPO'] = f"ssh://{username}@{host}:{full_path}"

        logger.debug(f"BORG_REPO set to {os.environ['BORG_REPO']}")

        # execute backup
        script_path = PurePosixPath(Path(__file__).resolve().parent) / f"{repo_name}.sh"
        try:
            proc = subprocess.Popen(
                [str(script_path)],
                env=os.environ,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            return_code = log_subprocess(proc, repo_name)

            if return_code == 0:
                logger.info(f"Backup for repo {repo_name} completed successfully")
            elif return_code == 1:
                logger.warning(f"Backup for repo {repo_name} completed with warnings")
            else:
                logger.critical(f"Backup for repo {repo_name} completed with errors. Aborting all backups")
                raise BackupError(f"Backup for repo {repo_name} completed with errors. Aborting all backups")

        except Exception as e:
            logger.critical(f"Unexpected exception during backup: {e}", exc_info=True)
            logger.critical(f"Backup for repo {repo_name} completed with errors. Aborting all backups")
            raise BackupError(f"Backup for repo {repo_name} completed with errors. Aborting all backups") from e

    else:
        logger.critical(f"Host not found. Failed to backup repo {repo_name}. Aborting all backups")
        raise BackupError(f"Host not found. Failed to backup repo {repo_name}. Aborting all backups")

