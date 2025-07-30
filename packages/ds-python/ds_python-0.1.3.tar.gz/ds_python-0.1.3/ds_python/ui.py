from typing import List

from dashing import HGauge, HSplit, Text, VSplit


def create_ui(data: List[dict]):
    widgets = []
    for obj in data:
        cpu_perc = obj['CPUPerc']
        mem_perc = obj['MemPerc']
        mem_usage = obj['MemUsage']
        net_io = obj['NetIO']
        block_io = obj['BlockIO']

        cpu_int = int(float(cpu_perc.replace('%', '')))
        mem_int = int(float(mem_perc.replace('%', '')))

        current_widget = VSplit(  # ui.items[0]
            VSplit(
                HSplit(
                    HGauge(
                        title=f'CPU {cpu_perc}',
                        val=cpu_int,
                        border_color=4,
                        color=1 if cpu_int >= 70 else 2,
                    ),
                    HGauge(
                        title=f'RAM {mem_perc}',
                        val=mem_int,
                        border_color=4,
                        color=1 if mem_int >= 70 else 2,
                    ),
                ),
                HSplit(
                    Text(
                        mem_usage, title='MemUsage', color=3, border_color=4
                    ),  # ui.items[0].items[0]
                    Text(
                        net_io, title='NetIO', color=3, border_color=4
                    ),  # ui.items[0].items[0]
                    Text(block_io, title='BlockIO', color=3, border_color=4),
                ),
            ),
            # ui.items[0].items[0]
            title=obj['Name'],
            border_color=3,
        )

        widgets.append(current_widget)

    return VSplit(*widgets)
