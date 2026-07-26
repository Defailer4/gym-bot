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


def _build_water_chart(data: list) -> io.BytesIO:
    dates = [datetime.strptime(row[0], "%Y-%m-%d") for row in data]
    amounts = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(8, 4.5))

    bars = ax.bar(dates, amounts, color='#17a2b8', width=0.5, edgecolor='black', alpha=0.8)

    ax.set_title("История потребления воды (за последние дни)", fontsize=14, fontweight='bold', pad=15)
    ax.set_ylabel("Объем (мл)", fontsize=11)
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)  # Сетка только по горизонтали

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate()

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f'{int(height)}',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha='center', va='bottom', fontsize=9, fontweight='bold'
        )

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    buf.seek(0)
    plt.close(fig)
    return buf


async def generate_water_chart(data: list) -> io.BytesIO:
    return await asyncio.to_thread(_build_water_chart, data)