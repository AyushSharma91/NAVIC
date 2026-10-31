import matplotlib.pyplot as plt
import folium


# render route line and start/end markers on a folium map
def create_route_map(df):
    if df.empty:
        return None

    start = [df.iloc[0]["Latitude"], df.iloc[0]["Longitude"]]
    route_map = folium.Map(location=start, zoom_start=16)

    coordinates = list(zip(df["Latitude"], df["Longitude"]))

    # draw route polyline
    folium.PolyLine(
        coordinates,
        color="blue",
        weight=5,
        opacity=0.8
    ).add_to(route_map)

    # start pin (green) and end pin (red)
    folium.Marker(
        coordinates[0],
        popup="Start",
        icon=folium.Icon(color="green")
    ).add_to(route_map)

    folium.Marker(
        coordinates[-1],
        popup="End",
        icon=folium.Icon(color="red")
    ).add_to(route_map)

    return route_map


# plot speed across gps points
def plot_speed(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["Speed(m/s)"], linewidth=2)
    ax.set_title("Speed Profile")
    ax.set_xlabel("GPS Point")
    ax.set_ylabel("Speed (m/s)")
    ax.grid(True)
    fig.tight_layout()
    return fig


# plot positioning accuracy across gps points
def plot_accuracy(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["Accuracy(m)"], linewidth=2)
    ax.set_title("GNSS Accuracy")
    ax.set_xlabel("GPS Point")
    ax.set_ylabel("Accuracy (m)")
    ax.grid(True)
    fig.tight_layout()
    return fig


# plot satellite signal strength (C/N0) over samples
def plot_signal_strength(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["Cn0DbHz"], linewidth=2)
    ax.set_title("Signal Strength")
    ax.set_xlabel("Satellite Sample")
    ax.set_ylabel("C/N0 (dB-Hz)")
    ax.grid(True)
    fig.tight_layout()
    return fig


# bar chart comparing average signal strength per constellation
def plot_constellation_comparison(df):
    grouped = df.groupby("ConstellationType")["Cn0DbHz"].mean()

    names = {
        1: "GPS",
        2: "SBAS",
        3: "GLONASS",
        4: "QZSS",
        5: "BeiDou",
        6: "Galileo",
        7: "NavIC"
    }

    labels = [names.get(i, str(i)) for i in grouped.index]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, grouped.values)
    ax.set_title("Average Signal Strength")
    ax.set_xlabel("Constellation")
    ax.set_ylabel("Average C/N0")
    fig.tight_layout()
    return fig