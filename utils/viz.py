import pandas as pd, matplotlib.pyplot as plt
from pathlib import Path

def save_forecast_chart(site_id, fc: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8,3))
    ax.plot(fc["ts_utc"], fc["y_p50"], label="P50")
    ax.fill_between(fc["ts_utc"], fc["y_p50"], fc["y_p90"], alpha=0.2, label="P90")
    ax.set_title(f"Arrivals forecast — {site_id}")
    ax.set_ylabel("arrivals/hour"); ax.set_xlabel("time (UTC)"); ax.legend()
    Path("outputs").mkdir(exist_ok=True)
    fig.autofmt_xdate()
    fig.savefig(f"outputs/forecast_{site_id}.png", bbox_inches="tight")
    plt.close(fig)
