import os
import pandas as pd

from src.config import (
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    ROUTE_DATA_FILE,
    SATELLITE_DATA_FILE,
    LOG_EXTENSION,
)


# parse Fix lines from gnss logger txt files
def parse_fix_records(file_path, trip_name):
    records = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line.startswith("Fix,"):
                continue

            parts = line.split(",")
            try:
                record = {
                    "Trip": trip_name,
                    "Provider": parts[1],
                    "Latitude": float(parts[2]),
                    "Longitude": float(parts[3]),
                    "Altitude": float(parts[4]),
                    "Speed(m/s)": float(parts[5]),
                    "Accuracy(m)": float(parts[6]),
                    "UnixTime": int(parts[8])
                }
                records.append(record)
            except (ValueError, IndexError):
                continue

    return records


# parse Status lines to get satellite info (constellation, svid, signal strength)
def parse_status_records(file_path, trip_name):
    records = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line.startswith("Status,"):
                continue

            parts = line.split(",")
            try:
                record = {
                    "Trip": trip_name,
                    "UnixTime": int(parts[1]),
                    "ConstellationType": int(parts[4]),
                    "Svid": int(parts[5]),
                    "Cn0DbHz": float(parts[7])
                }
                records.append(record)
            except (ValueError, IndexError):
                continue

    return records


# loop over all raw txt log files and save route and satellite csv files
def parse_all_logs():
    route_records = []
    satellite_records = []

    files = os.listdir(DATA_RAW_DIR)

    for file in files:
        if not file.endswith(LOG_EXTENSION):
            continue

        trip_name = os.path.splitext(file)[0]
        file_path = os.path.join(DATA_RAW_DIR, file)

        print(f"\nReading : {file}")
        fix = parse_fix_records(file_path, trip_name)
        status = parse_status_records(file_path, trip_name)

        print(f"Fix Records    : {len(fix)}")
        print(f"Status Records : {len(status)}")

        route_records.extend(fix)
        satellite_records.extend(status)

    route_df = pd.DataFrame(route_records)
    satellite_df = pd.DataFrame(satellite_records)

    route_path = os.path.join(DATA_PROCESSED_DIR, ROUTE_DATA_FILE)
    satellite_path = os.path.join(DATA_PROCESSED_DIR, SATELLITE_DATA_FILE)

    route_df.to_csv(route_path, index=False)
    satellite_df.to_csv(satellite_path, index=False)

    print("\n===================================")
    print("Datasets Created Successfully")
    print("-----------------------------------")
    print(f"Route Records     : {len(route_df)}")
    print(f"Satellite Records : {len(satellite_df)}")
    print("-----------------------------------")
    print(route_path)
    print(satellite_path)
    print("===================================")


if __name__ == "__main__":
    parse_all_logs()