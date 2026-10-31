import os
import pandas as pd
from geopy.distance import geodesic

from src.config import (
    DATA_PROCESSED_DIR,
    ROUTE_DATA_FILE,
    SATELLITE_DATA_FILE,
)


# load the processed route csv file
def load_dataset():
    path = os.path.join(DATA_PROCESSED_DIR, ROUTE_DATA_FILE)
    if not os.path.exists(path):
        return None
    return pd.read_csv(path)


# load satellite records
def load_satellite_dataset():
    path = os.path.join(DATA_PROCESSED_DIR, SATELLITE_DATA_FILE)
    if not os.path.exists(path):
        return None
    return pd.read_csv(path)


# calculate total route distance in meters between consecutive GPS coordinates
def calculate_distance(df):
    if len(df) < 2:
        return 0

    distance = 0
    coordinates = list(zip(df["Latitude"], df["Longitude"]))

    # add distance between each consecutive point
    for i in range(1, len(coordinates)):
        distance += geodesic(coordinates[i - 1], coordinates[i]).meters

    return distance


# get metrics (distance, time, speed, accuracy) for a single trip
def analyze_trip(df):
    distance = calculate_distance(df)

    # duration converted from milliseconds to seconds
    duration = (df["UnixTime"].max() - df["UnixTime"].min()) / 1000

    avg_speed = df["Speed(m/s)"].mean()
    max_speed = df["Speed(m/s)"].max()
    avg_accuracy = df["Accuracy(m)"].mean()

    summary = {
        "Trip": df.iloc[0]["Trip"],
        "Distance (m)": round(distance, 2),
        "Duration (s)": round(duration, 2),
        "Average Speed (m/s)": round(avg_speed, 2),
        "Maximum Speed (m/s)": round(max_speed, 2),
        "Average Accuracy (m)": round(avg_accuracy, 2)
    }

    return summary


# iterate over all trips and print out their stats
def analyze_routes(route_df):
    print("\n========== ROUTE ANALYSIS ==========\n")
    summaries = []
    trips = route_df["Trip"].unique()

    for trip in trips:
        trip_df = route_df[route_df["Trip"] == trip].reset_index(drop=True)
        summary = analyze_trip(trip_df)
        summaries.append(summary)

        print(f"Trip : {summary['Trip']}")
        print(f"Distance : {summary['Distance (m)']} m")
        print(f"Duration : {summary['Duration (s)']} sec")
        print(f"Average Speed : {summary['Average Speed (m/s)']} m/s")
        print(f"Maximum Speed : {summary['Maximum Speed (m/s)']} m/s")
        print(f"Average Accuracy : {summary['Average Accuracy (m)']} m")
        print("-" * 40)

    return pd.DataFrame(summaries)


# summarize satellite count and average signal (Cn0) by constellation
def analyze_satellites(df):
    print("\n========== SATELLITE ANALYSIS ==========\n")

    # android constellation type mapping
    constellation_names = {
        1: "GPS",
        2: "SBAS",
        3: "GLONASS",
        4: "QZSS",
        5: "BeiDou",
        6: "Galileo",
        7: "NavIC"
    }

    results = []
    for constellation in sorted(df["ConstellationType"].unique()):
        data = df[df["ConstellationType"] == constellation]
        result = {
            "Constellation": constellation_names.get(constellation, f"Unknown ({constellation})"),
            "Unique Satellites": data["Svid"].nunique(),
            "Average Signal": round(data["Cn0DbHz"].mean(), 2)
        }
        results.append(result)

    satellite_summary = pd.DataFrame(results)
    print(satellite_summary)
    return satellite_summary


# run both route and satellite analysis
def run_analysis():
    route_df = load_dataset()
    satellite_df = load_satellite_dataset()

    if route_df is None:
        print("Route dataset not found.")
        return

    route_summary = analyze_routes(route_df)
    satellite_summary = None

    if satellite_df is not None:
        satellite_summary = analyze_satellites(satellite_df)

    return (
        route_df,
        satellite_df,
        route_summary,
        satellite_summary
    )


if __name__ == "__main__":
    run_analysis()