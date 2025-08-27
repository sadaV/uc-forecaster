from .agents import SignalsAgent, FeatureStoreAgent, ForecasterAgent, PlannerAgent, BriefingAgent

class UCPlannerFlow:
    def __init__(self):
        self.signals = SignalsAgent()
        self.fstore  = FeatureStoreAgent()
        self.forecast= ForecasterAgent()
        self.planner = PlannerAgent()
        self.brief   = BriefingAgent()

    def run(self, site_id: str, horizon: int = 12):
        state = {"site_id": site_id, "horizon": horizon}
        state.update(self.signals.handle(state))
        state.update(self.fstore.handle({**state, **state}))
        state.update(self.forecast.handle(state))
        state.update(self.planner.handle(state))
        state.update(self.brief.handle(state))
        return state  # contains signals_df, features_df, forecast_df, plan_df, brief_md
