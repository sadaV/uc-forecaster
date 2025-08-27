import argparse, pandas as pd
from pathlib import Path
from strands_app.flow import UCPlannerFlow

def save_outputs(site_id, fc, plan, md):
    Path("outputs").mkdir(exist_ok=True)
    fc.to_csv(f"outputs/forecast_{site_id}.csv", index=False)
    plan.to_json(f"outputs/plan_{site_id}.json", orient="records", indent=2)
    Path(f"outputs/briefing_{site_id}.md").write_text(md)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True)
    ap.add_argument("--horizon", type=int, default=12)
    args = ap.parse_args()

    flow = UCPlannerFlow()
    result = flow.run(args.site, args.horizon)
    save_outputs(args.site, result["forecast_df"], result["plan_df"], result["brief_md"])
    print("\nBriefing:\n")
    print(result["brief_md"])
