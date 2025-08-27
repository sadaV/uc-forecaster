import pandas as pd, math

class PlannerAgent:
    """Converts forecasts into staffing/actions using tiny queueing heuristics."""
    def run(self, forecast_df: pd.DataFrame):
        plan = []
        for _, row in forecast_df.iterrows():
            demand = row.y_p50
            providers = 1 if demand < 8 else 2 if demand < 16 else 3
            rooms = max(2, providers + 1)
            note = (f"{row.ts_utc:%H:%M} → expect ~{int(round(demand))} "
                    f"arrivals (P90≈{int(round(row.y_p90))}). "
                    f"Staff {providers} provider(s), open {rooms} rooms.")
            plan.append({"site_id":row.site_id, "ts_utc":str(row.ts_utc),
                         "providers":int(providers), "rooms":int(rooms), "note":note})
        return pd.DataFrame(plan)
