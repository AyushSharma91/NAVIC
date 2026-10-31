# AI Powered Smart Route Analyzer

A B.Tech mini project that turns GNSS/NavIC logs collected from a smartphone into an AI-powered route analysis tool.

## What it does

This project takes real GNSS logs recorded with a GPS Logger app during actual trips and builds:

- **Trip analysis** — total distance traveled, trip duration, average and maximum speed, and positioning accuracy for every recorded trip.
- **Satellite analysis** — which constellations (NavIC, GPS, GLONASS, BeiDou, Galileo, etc.) were tracked, how many satellites were visible, and their average signal strength (C/N0).
- **Machine learning** — a Random Forest regressor trained on coordinates, speed, and altitude to predict GPS accuracy at any point in meters.
- **Visualization** — an interactive route map with start/end markers, plus speed, accuracy, and satellite signal charts.
- **Dashboard** — a Streamlit UI to browse trips, view maps and analytics, inspect satellite details, and get live AI predictions of positioning accuracy.

In short: it converts phone-collected GPS/NavIC logs into a trip analyzer, a signal-quality reporter for Indian NavIC, and an ML model that predicts location accuracy.

## Pipeline

```
main.py
  1. Parse    src/parser.py          raw .txt GNSS logs -> processed CSVs
  2. Analyze  src/analysis.py        trip metrics + satellite statistics
  3. Train    src/model.py           Random Forest model on route coordinates
```

## Project structure

```
NAVIC/
├── main.py                 # run the full pipeline (parse -> analyze -> train)
├── README.md
├── dashboard/
│   └── app1.py             # Streamlit dashboard
├── data/
│   ├── raw/                # input GNSS logger .txt logs
│   └── processed/          # generated CSV datasets
├── src/
│   ├── config.py           # paths and constants
│   ├── parser.py           # log parsing
│   ├── analysis.py         # route/satellite analysis
│   ├── model.py            # ML training, saving and loading
│   └── visualization.py    # folium maps and matplotlib plots
└── output/
    ├── maps/               # generated route maps
    ├── graphs/             # generated plots
    └── models/             # saved Random Forest model
```

## Setup

```bash
pip install -r requirements.txt
```

Dependencies: `pandas`, `numpy`, `geopy`, `scikit-learn`, `matplotlib`, `folium`, `joblib`, `streamlit`.

## Usage

1. Drop GNSS Logger `.txt` log files into `data/raw/`.
2. Run the full pipeline:

   ```bash
   python main.py
   ```

3. Launch the dashboard:

   ```bash
   streamlit run dashboard/app1.py
   ```

The dashboard tabs are:

- **Route** — interactive map of the selected trip with start/end markers.
- **Analytics** — trip statistics and speed/accuracy charts.
- **NavIC** — satellite breakdown and constellation signal comparison.
- **AI** — live predicted GPS accuracy from entered coordinates.

## How to add data

GNSS logs are standard `.txt` exports from the "GPS Logger" Android app. Fix records provide coordinates, altitude, speed, accuracy, and timestamps; Status records provide satellite constellation, SVID, and C/N0 signal strength.