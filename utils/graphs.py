import io
import asyncio
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

matplotlib.use('Agg')

def _build_weight_chart(data: list) -> io.BytesIO:
    dates = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in data]
    weights = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(8,4.5))

    ax.plot(dates, weights, marker='o', linestyle='-', color='#007bf5', linewidth=2, markersize=6)

    ax.set_title("Динамика изменения веса", fontsize=14, fontweight='bold', pad=15)
    ax.set_ylabel("Вес (кг)", fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.5)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    buf.seek(0)
    plt.close(fig)
    return buf


async def generate_weight_chart(data: list) -> io.BytesIO:
    return await asyncio.to_thread(_build_weight_chart, data)