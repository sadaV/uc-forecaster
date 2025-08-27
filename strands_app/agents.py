from agents.signals_agent import SignalsAgent as _Signals
from agents.feature_store_agent import FeatureStoreAgent as _FS
from agents.forecaster_agent import ForecasterAgent as _FC
from agents.planner_agent import PlannerAgent as _PL
from agents.briefing_agent import BriefingAgent as _BR

class SignalsAgent:
    def __init__(self): self.inner = _Signals()
    def handle(self, payload):  # payload = {"site_id": "...", "horizon": 12}
        df = self.inner.run(payload["site_id"], payload.get("horizon", 12))
        return {"signals_df": df}

class FeatureStoreAgent:
    def __init__(self): self.inner = _FS()
    def handle(self, payload):
        df = self.inner.run(payload["site_id"], payload["signals_df"])
        return {"features_df": df}

class ForecasterAgent:
    def __init__(self): self.inner = _FC()
    def handle(self, payload):
        fc = self.inner.run(payload["features_df"])
        return {"forecast_df": fc}

class PlannerAgent:
    def __init__(self): self.inner = _PL()
    def handle(self, payload):
        plan = self.inner.run(payload["forecast_df"])
        return {"plan_df": plan}

class BriefingAgent:
    def __init__(self): self.inner = _BR()
    def handle(self, payload):
        merged = payload["forecast_df"].merge(
            payload["features_df"][["site_id","ts_utc","precip_flag","is_holiday"]],
            on=["site_id","ts_utc"], how="left"
        )
        md = self.inner.run(payload["site_id"], merged, payload["plan_df"])
        return {"brief_md": md}
