# UC Forecaster – Agentic AI Demo  

This repo is a **small but meaningful PoC** that shows how to use **AI agents** and **AWS Strands** to solve a real operational problem:  
> *How can an urgent care center forecast patient demand and plan staffing accordingly?*  

The demo uses **five cooperating agents**:  

- **Signals Agent** → collects signals (synthetic weather, calendar, staffing).  
- **Feature Store Agent** → cleans & structures the data.  
- **Forecaster Agent** → predicts demand with XGBoost.  
- **Planner Agent** → converts predictions into staffing actions.  
- **Briefing Agent** → produces a human-readable briefing.  

Together, they behave like a **team of microservices** in an agentic flow.  

---

## 🚀 Quickstart (Local, No AWS Required)

1. **Clone & install**
     ```bash   
     git clone https://github.com/sadaV/uc-forecaster.git
     cd uc-forecaster
     python3 -m venv .venv && source .venv/bin/activate
     pip install -r requirements.txt
     ```
3. **Generate synthetic data**
     ```bash   
      python scripts/make_synth_data.py
     ```

5. **Train the forecasting model**
     ```bash
    python model/train_xgb.py
     ```

7. **Run the pipeline (sequential app)**
   ```bash
    python app.py --site UC-AUS-01 --horizon 12
   ```

9. **Run with Strands orchestration**
    ```bash
    python run_strands.py --site UC-AUS-01 --horizon 12
    ```


**Outputs are written to**   
__outputs/:__  
&nbsp;&nbsp;&nbsp;&nbsp;forecast_<site>.csv   
 &nbsp;&nbsp;&nbsp;&nbsp;plan_<site>.json  
&nbsp;&nbsp;&nbsp;&nbsp;briefing_<site>.md  

---

## 📝 Example Briefing Output

📍 Site UC-AUS-01  
Forecast window: 08:00–20:00 UTC  
Expected demand: ~116 arrivals (P50)  
Peak around 14:00 with ~18 arrivals  
Key factors: holiday  
  
Recommended actions:  
- Add one PA to triage from 13:00–15:00  
- Open Room 6 for overflow  

