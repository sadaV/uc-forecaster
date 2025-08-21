import pandas as pd, numpy as np, xgboost as xgb, json, os
from pathlib import Path

DATA = Path("data"); ART = Path("model/artifacts"); ART.mkdir(parents=True, exist_ok=True)

def load():
    a = pd.read_csv(DATA/"arrivals_train.csv", parse_dates=["ts_utc"])
    w = pd.read_csv(DATA/"weather_hourly.csv", parse_dates=["ts_utc"])
    o = pd.read_csv(DATA/"ops_schedule.csv", parse_dates=["ts_utc"])
    c = pd.read_csv(DATA/"calendar.csv", parse_dates=["date"])
    a["date"] = a.ts_utc.dt.normalize()
    a = a.merge(w, on=["site_id","ts_utc"]).merge(o, on=["site_id","ts_utc"])
    c["date"] = pd.to_datetime(c["date"], utc=True)
    a = a.merge(c, left_on="date", right_on="date", how="left")
    a["hour"] = a.ts_utc.dt.hour
    a["dow"]  = a.ts_utc.dt.dayofweek
    a["y"] = a["arrivals"].astype(float)
    a.sort_values(["site_id","ts_utc"], inplace=True)
    a["lag1h"] = a.groupby("site_id")["y"].shift(1)
    a["lag24h"] = a.groupby("site_id")["y"].shift(24)
    a["roll6h"] = a.groupby("site_id")["y"].rolling(6).mean().reset_index(0,drop=True)
    a.dropna(inplace=True)
    return a

def train(df):
    feats = ["hour","dow","is_holiday","school_in_session_flag","temp_c","precip_flag",
             "rooms_staffed","providers_on_shift","lag1h","lag24h","roll6h"]
    X = df[feats]; y = df["y"]
    dtrain = xgb.DMatrix(X, label=y)
    params = {"max_depth":4,"eta":0.1,"min_child_weight":2,"subsample":0.9,"colsample_bytree":0.9,
              "objective":"reg:squarederror","eval_metric":"rmse","seed":7}
    bst = xgb.train(params, dtrain, num_boost_round=300)
    bst.save_model(str(ART/"booster.json"))
    (ART/"features.json").write_text(json.dumps(feats))
    print("Saved model & features to model/artifacts/")
    return bst, feats

if __name__ == "__main__":
    df = load()
    train(df)
