import pandas as pd

class FeatureStoreAgent:
    """Builds model-ready features with lags/rollups using historical arrivals."""
    def run(self, site_id: str, signals_df: pd.DataFrame):
        a = pd.read_csv("data/arrivals_train.csv", parse_dates=["ts_utc"])
        hist = a[a.site_id==site_id].sort_values("ts_utc").copy()
        hist["y"] = hist["arrivals"].astype(float)
        hist["lag1h"]  = hist["y"].shift(1)
        hist["lag24h"] = hist["y"].shift(24)
        hist["roll6h"] = hist["y"].rolling(6).mean()
        hist["hour"] = hist.ts_utc.dt.hour
        hist["dow"]  = hist.ts_utc.dt.dayofweek
        # take last known row to seed lags, then append future timestamps with NA y
        last = hist.iloc[-1:].copy()
        fut = signals_df.copy()
        fut["hour"] = fut.ts_utc.dt.hour
        fut["dow"]  = fut.ts_utc.dt.dayofweek
        # propagate last known lag values for MVP
        fut["lag1h"] = last["y"].values[0]
        fut["lag24h"] = hist.iloc[-24:]["y"].mean() if len(hist)>=24 else last["y"].values[0]
        fut["roll6h"] = hist.iloc[-6:]["y"].mean() if len(hist)>=6 else last["y"].values[0]
        cols = ["site_id","ts_utc","hour","dow","is_holiday","school_in_session_flag",
                "temp_c","precip_flag","rooms_staffed","providers_on_shift",
                "lag1h","lag24h","roll6h"]
        return fut[cols]
