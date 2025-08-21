import json, xgboost as xgb, pandas as pd
from pathlib import Path

ART = Path("model/artifacts")

class ForecasterAgent:
    def __init__(self):
        self.model = xgb.Booster()
        self.model.load_model(str(ART/"booster.json"))
        self.features = json.loads((ART/"features.json").read_text())

    def run(self, features_df: pd.DataFrame):
        d = xgb.DMatrix(features_df[self.features])
        p50 = self.model.predict(d)
        # simple uncertainty band: +40% as P90 (upgrade later to quantile model)
        p90 = p50 * 1.4
        out = features_df[["site_id","ts_utc"]].copy()
        out["y_p50"] = p50.clip(0).round(1)
        out["y_p90"] = p90.clip(0).round(1)
        return out
