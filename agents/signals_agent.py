import pandas as pd

class SignalsAgent:
    """Loads latest slices of signals for a site & horizon."""
    def run(self, site_id: str, horizon_hours: int = 12):
        a = pd.read_csv("data/arrivals_train.csv", parse_dates=["ts_utc"])
        w = pd.read_csv("data/weather_hourly.csv", parse_dates=["ts_utc"])
        o = pd.read_csv("data/ops_schedule.csv", parse_dates=["ts_utc"])
        c = pd.read_csv("data/calendar.csv", parse_dates=["date"])
        last_ts = a[a.site_id==site_id].ts_utc.max()
        future_idx = pd.date_range(last_ts + pd.Timedelta(hours=1),
                                   periods=horizon_hours, freq="H", tz="UTC")
        # naive future signals: repeat last known ops/weather for simplicity (MVP)
        base = pd.DataFrame({"site_id":site_id, "ts_utc":future_idx})
        last_w = w[(w.site_id==site_id) & (w.ts_utc==last_ts)].tail(1)
        last_o = o[(o.site_id==site_id) & (o.ts_utc==last_ts)].tail(1)
        # broadcast last row values forward
        base = base.merge(last_w.drop(columns=["ts_utc"]), on="site_id", how="left")
        base = base.merge(last_o.drop(columns=["ts_utc"]), on="site_id", how="left")
        base["date"] = base.ts_utc.dt.normalize()
        c["date"] = pd.to_datetime(c["date"]).dt.normalize()
        base = base.merge(c, on="date", how="left")
        return base[["site_id","ts_utc","temp_c","precip_flag","rooms_staffed",
                     "providers_on_shift","is_holiday","school_in_session_flag"]]
