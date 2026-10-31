import os
import streamlit as st
import joblib

from src.analysis import (
    load_dataset,
    load_satellite_dataset,
    calculate_distance
)

from src.visualization import (
    create_route_map,
    plot_speed,
    plot_accuracy,
    plot_signal_strength,
    plot_constellation_comparison
)

from src.config import (
    MODELS_DIR,
    MODEL_FILE
)


# basic page setup
st.set_page_config(
    page_title="AI Powered Smart Route Analyzer",
    page_icon="🛰️",
    layout="wide"
)

st.title("🛰️ AI Powered Smart Route Analyzer")
st.write("Route Analysis using GNSS Logs collected from a NavIC-enabled smartphone.")

# load preprocessed datasets
route_df = load_dataset()
satellite_df = load_satellite_dataset()

if route_df is None:
    st.error("Run main.py first.")
    st.stop()

# sidebar for trip selection
st.sidebar.title("Navigation")
trip_names = sorted(route_df["Trip"].unique())
selected_trip = st.sidebar.selectbox("Select Trip", trip_names)

trip_df = route_df[route_df["Trip"] == selected_trip].reset_index(drop=True)

# calculate summary stats for the selected trip
distance = calculate_distance(trip_df)
duration = (trip_df["UnixTime"].max() - trip_df["UnixTime"].min()) / 1000
average_speed = trip_df["Speed(m/s)"].mean()
maximum_speed = trip_df["Speed(m/s)"].max()
average_accuracy = trip_df["Accuracy(m)"].mean()

# tabbed interface
tab1, tab2, tab3, tab4 = st.tabs(["🗺 Route", "📊 Analytics", "🛰 NavIC", "🤖 AI"])

# tab 1: interactive folium route map
with tab1:
    st.subheader(selected_trip)
    route_map = create_route_map(trip_df)
    st.components.v1.html(route_map._repr_html_(), height=600)

# tab 2: trip telemetry and speed/accuracy graphs
with tab2:
    st.subheader("Trip Statistics")
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)

    c1.metric("Distance", f"{distance:.2f} m")
    c2.metric("Duration", f"{duration:.2f} sec")
    c3.metric("Average Speed", f"{average_speed:.2f} m/s")
    c4.metric("Average Accuracy", f"{average_accuracy:.2f} m")

    st.divider()

    st.subheader("Speed")
    speed_fig = plot_speed(trip_df)
    st.pyplot(speed_fig)

    st.divider()

    st.subheader("Accuracy")
    accuracy_fig = plot_accuracy(trip_df)
    st.pyplot(accuracy_fig)

# tab 3: satellite breakdown and signal comparison
with tab3:
    st.subheader("Satellite Analysis")
    if satellite_df is None:
        st.warning("No satellite data available.")
    else:
        trip_sat = satellite_df[satellite_df["Trip"] == selected_trip].copy()

        constellation_names = {
            1: "GPS",
            2: "SBAS",
            3: "GLONASS",
            4: "QZSS",
            5: "BeiDou",
            6: "Galileo",
            7: "NavIC"
        }
        trip_sat["Constellation"] = trip_sat["ConstellationType"].map(constellation_names)

        st.dataframe(trip_sat[["Svid", "Constellation", "Cn0DbHz"]])

        st.subheader("Signal Strength")
        signal_fig = plot_signal_strength(trip_sat)
        st.pyplot(signal_fig)

        st.subheader("Constellation Comparison")
        comparison = plot_constellation_comparison(trip_sat)
        st.pyplot(comparison)

# tab 4: live machine learning prediction using random forest
with tab4:
    st.subheader("Machine Learning")
    model_path = os.path.join(MODELS_DIR, MODEL_FILE)

    if not os.path.exists(model_path):
        st.warning("Train the model first.")
    else:
        model = joblib.load(model_path)

        latitude = st.number_input("Latitude", value=float(trip_df.iloc[0]["Latitude"]))
        longitude = st.number_input("Longitude", value=float(trip_df.iloc[0]["Longitude"]))
        altitude = st.number_input("Altitude", value=float(trip_df.iloc[0]["Altitude"]))
        speed = st.number_input("Speed", value=float(trip_df.iloc[0]["Speed(m/s)"]))

        if st.button("Predict Accuracy"):
            prediction = model.predict([[latitude, longitude, altitude, speed]])
            st.success(f"Predicted Accuracy : {prediction[0]:.2f} meters")

st.divider()
st.caption("AI Powered Smart Route Analyzer | B.Tech Mini Project")