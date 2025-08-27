import pandas as pd, textwrap, os

USE_LLM = False  # set True when you wire Bedrock creds

class BriefingAgent:
    def __init__(self): pass

    def _llm(self, prompt:str)->str:
        # Placeholder; wire to Bedrock Claude/Nova later.
        return f"(LLM would write a concise ops briefing here)\n\n{prompt}"

    def run(self, site_id: str, forecast_df: pd.DataFrame, plan_df: pd.DataFrame):
        # Time window of forecast
        start = forecast_df.ts_utc.min().strftime("%H:%M")
        end   = forecast_df.ts_utc.max().strftime("%H:%M")
        window = f"{start}–{end} UTC"
    
        # Drivers (basic signals)
        drivers = []
        if "precip_flag" in forecast_df.columns and forecast_df["precip_flag"].mean() > 0:
            drivers.append("precipitation")
        if "is_holiday" in forecast_df.columns and forecast_df["is_holiday"].any():
            drivers.append("holiday")
        driver_txt = ", ".join(drivers) if drivers else "a typical weekday pattern"
    
        # Basic stats
        total_demand = int(forecast_df.y_p50.sum())
        peak_row = forecast_df.loc[forecast_df.y_p50.idxmax()]
        peak_hour = peak_row.ts_utc.strftime("%H:%M")
        peak_val = int(peak_row.y_p50)
    
        # Build summary text
        summary = (
            f"📍 Site {site_id}\n"
            f"Forecast window: {window}\n"
            f"Expected demand: ~{total_demand} arrivals (P50)\n"
            f"Peak around {peak_hour} with ~{peak_val} arrivals\n"
            f"Key factors: {driver_txt}\n\n"
            f"Recommended actions:\n"
        )
    
        # Actions from planner
        actions = "\n".join([f"- {row['note']}" for _, row in plan_df.iterrows()])
    
        return summary + actions

