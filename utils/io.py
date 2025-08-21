from pathlib import Path
def save_outputs(site_id, forecast_df, plan_df, briefing_md):
    out = Path("outputs"); out.mkdir(exist_ok=True)
    forecast_df.to_csv(out/f"forecast_{site_id}.csv", index=False)
    plan_df.to_json(out/f"plan_{site_id}.json", orient="records", indent=2)
    (out/f"briefing_{site_id}.md").write_text(briefing_md)
