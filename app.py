import argparse, pandas as pd
from agents.signals_agent import SignalsAgent
from agents.feature_store_agent import FeatureStoreAgent
from agents.forecaster_agent import ForecasterAgent
from agents.planner_agent import PlannerAgent
from agents.briefing_agent import BriefingAgent
from utils.viz import save_forecast_chart
from utils.io import save_outputs

def main(site_id:str, horizon:int):
    sig = SignalsAgent().run(site_id, horizon)
    feats = FeatureStoreAgent().run(site_id, sig)
    fc   = ForecasterAgent().run(feats)
    plan = PlannerAgent().run(fc)
    merged = fc.merge(
        feats[["site_id", "ts_utc", "precip_flag", "is_holiday"]],
        on=["site_id", "ts_utc"],
        how="left"
    )
    brief = BriefingAgent().run(site_id, merged, plan)
    save_outputs(site_id, fc, plan, brief)
    save_forecast_chart(site_id, fc)
    print("Forecast & plan ready ✅")
    print("\nBriefing:\n")
    print(brief)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True)
    ap.add_argument("--horizon", type=int, default=12)
    args = ap.parse_args()
    main(args.site, args.horizon)
