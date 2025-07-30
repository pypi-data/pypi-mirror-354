import subprocess
from logging import Logger


def exec_subprocess(command: str, log: Logger) -> subprocess.CompletedProcess:
    log.info(f"Executing command: {command}")
    process = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        log.error(f"Command {command} failed with: {process.stderr}")
        raise subprocess.CalledProcessError(
            returncode=process.returncode,
            cmd=command,
        )

    return process
