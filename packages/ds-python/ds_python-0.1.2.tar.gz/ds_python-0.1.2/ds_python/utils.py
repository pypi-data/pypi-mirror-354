import re
from subprocess import run

COMMAND_STATS = ['docker', 'stats', '--no-stream', '--format', 'json']
ANSI_ESPACE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')


def run_stats():
    return run(
        COMMAND_STATS,
        capture_output=True,
        universal_newlines=True,
        check=False,
    )


def clean_stdout(line: str):
    return ANSI_ESPACE.sub('', line).strip()
