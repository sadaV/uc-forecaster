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
    
        # 1) Signals
        sig_out = self.signals.handle(state)                 
        state.update(sig_out)
    
        # 2) Feature store
        fs_out = self.fstore.handle({
            "site_id": state["site_id"],
            "signals_df": state["signals_df"],
        })                                                   
        state.update(fs_out)
    
        # 3) Forecast
        fc_out = self.forecast.handle({"features_df": state["features_df"]})
        state.update(fc_out)                                 
    
        # 4) Planner
        plan_out = self.planner.handle({"forecast_df": state["forecast_df"]})
        state.update(plan_out)                              
    
        # 5) Briefing
        brief_out = self.brief.handle({
            "site_id": state["site_id"],
            "forecast_df": state["forecast_df"],
            "features_df": state["features_df"],  # for precip/holiday flags
            "plan_df": state["plan_df"],
        })                                                   
        state.update(brief_out)
    
        return state

