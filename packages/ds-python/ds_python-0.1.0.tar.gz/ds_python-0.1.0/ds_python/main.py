import json
import time

from rich.console import Console

from ds_python.ui import create_ui
from ds_python.utils import run_stats

console = Console()


def main():
    while True:
        try:
            stats = run_stats()
            lines = stats.stdout.split('\n')
            with console.status('Waiting for Containers...'):
                while len(lines) <= 1 and '' in lines:
                    console.clear()
                    time.sleep(1)
                    stats = run_stats()
                    lines = stats.stdout.split('\n')

            lines = [json.loads(line) for line in lines if line]
            ui = create_ui(lines)
            ui.display()
            time.sleep(0.5)

        except KeyboardInterrupt:
            break
