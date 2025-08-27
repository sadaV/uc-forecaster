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
    
        print("\n🚀 Starting UCPlannerFlow for site:", site_id)
        print("=========================================")
        time.sleep(0.5)

        # 1) Signals
        print("\n[1/5] 🔎 Collecting signals...")
        sig_out = self.signals.handle(state)
        state.update(sig_out)
        print(f"    ✓ Signals ready: {len(state['signals_df'])} rows")
        time.sleep(0.5)

        # 2) Feature store
        print("\n[2/5] 🗂️  Building feature set...")
        fs_out = self.fstore.handle({
            "site_id": state["site_id"],
            "signals_df": state["signals_df"],
        })
        state.update(fs_out)
        print(f"    ✓ Features ready: {len(state['features_df'].columns)} features")
        time.sleep(0.5)

        # 3) Forecast
        print("\n[3/5] 📈 Running forecast model (XGBoost)...")
        fc_out = self.forecast.handle({"features_df": state["features_df"]})
        state.update(fc_out)
        print(f"    ✓ Forecast ready: {len(state['forecast_df'])} horizon steps")
        time.sleep(0.5)

        # 4) Planner
        print("\n[4/5] 📋 Creating staffing plan...")
        plan_out = self.planner.handle({"forecast_df": state["forecast_df"]})
        state.update(plan_out)
        print(f"    ✓ Plan ready: {len(state['plan_df'])} recommendations")
        time.sleep(0.5)

        # 5) Briefing
        print("\n[5/5] 🗨️  Generating briefing...")
        brief_out = self.brief.handle({
            "site_id": state["site_id"],
            "forecast_df": state["forecast_df"],
            "features_df": state["features_df"],  # for precip/holiday flags
            "plan_df": state["plan_df"],
        })
        state.update(brief_out)
        print("    ✓ Briefing generated")
        time.sleep(0.5)

        print("\n✅ Flow complete! Results available in outputs/")
    
        return state
    
