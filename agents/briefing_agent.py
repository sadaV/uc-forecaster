import pandas as pd, textwrap, os

USE_LLM = False  # set True when you wire Bedrock creds

class BriefingAgent:
    def __init__(self): pass

    def _llm(self, prompt:str)->str:
        # Placeholder; wire to Bedrock Claude/Nova later.
        return f"(LLM would write a concise ops briefing here)\n\n{prompt}"

    def run(self, site_id:str, forecast_df: pd.DataFrame, plan_df: pd.DataFrame):
        window = f"{forecast_df.ts_utc.min():%H:%M}–{forecast_df.ts_utc.max():%H:%M} UTC"
        drivers = []
        if "precip_flag" in forecast_df.columns and forecast_df.precip_flag.mean()>0:
            drivers.append("precipitation")
        if "is_holiday" in forecast_df.columns and forecast_df.is_holiday.any():
            drivers.append("holiday")
        driver_txt = ", ".join(drivers) if drivers else "typical weekday pattern"

        summary = (
            f"Site **{site_id}** — Next 12h ({window})\n"
            f"- Demand (P50): {int(forecast_df.y_p50.sum())} arrivals total\n"
            f"- Peak hour: {forecast_df.loc[forecast_df.y_p50.idxmax()].ts_utc:%H:%M} "
            f"with ~{int(forecast_df.y_p50.max())} arrivals\n"
            f"- Likely drivers: {driver_txt}\n"
            f"- Actions:\n"
        )
        actions = "\n".join([f"  • {r['note']}" for _, r in plan_df.iterrows()])
        md = summary + actions
        if USE_LLM:
            return self._llm(md)
        return md  # plain summary for MVP
