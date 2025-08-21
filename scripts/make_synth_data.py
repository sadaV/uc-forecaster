import numpy as np, pandas as pd
rng = np.random.default_rng(7)

SITES = ["UC-AUS-01","UC-SEA-02"]
start = pd.Timestamp.utcnow().floor("H") - pd.Timedelta(days=70)
hours = pd.date_range(start, periods=70*24, freq="H", tz="UTC")

def mk_arrivals(site):
    base = 6 + 3*np.sin(2*np.pi*(hours.hour)/24) + 2*(hours.dayofweek>=5)  # weekend bump
    weather_noise = rng.normal(0,1, size=len(hours))
    precip = rng.choice([0,1], p=[0.8,0.2], size=len(hours))
    holiday = ((hours.month==7) & (hours.day==4)).astype(int)
    ops = pd.Series( ( (hours.hour>=8)&(hours.hour<=20) ).astype(int)*2 + 1 )
    lam = np.clip(base + 1.5*precip + 2*holiday + 0.2*weather_noise + 0.5*ops, 0.2, None)
    y = rng.poisson(lam)
    return pd.DataFrame({"site_id":site,"ts_utc":hours, "arrivals":y})

arrivals = pd.concat([mk_arrivals(s) for s in SITES], ignore_index=True)
arrivals.to_csv("data/arrivals_train.csv", index=False)

weather = (arrivals[["site_id","ts_utc"]]
           .assign(temp_c = 20 + 10*np.sin(2*np.pi*(arrivals.ts_utc.dt.hour)/24) + rng.normal(0,2,len(arrivals)),
                   precip_flag = rng.choice([0,1], p=[0.8,0.2], size=len(arrivals))))
weather.to_csv("data/weather_hourly.csv", index=False)

ops = (arrivals[["site_id","ts_utc"]]
       .assign(rooms_staffed = ((arrivals.ts_utc.dt.hour.between(8,20)).astype(int)+1),
               providers_on_shift = ((arrivals.ts_utc.dt.hour.between(8,20)).astype(int)+1)))
ops.to_csv("data/ops_schedule.csv", index=False)

cal = pd.DataFrame({"date": pd.date_range(hours.min().date(), hours.max().date(), freq="D")})
cal["is_holiday"] = ((cal.date.dt.month==7)&(cal.date.dt.day==4)).astype(int)
cal["school_in_session_flag"] = (~cal.date.dt.month.isin([6,7,8])).astype(int)
cal.to_csv("data/calendar.csv", index=False)

print("Synthetic CSVs written to data/")
