import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Constants
MAX_SPEED = 240
MAX_RPM = 8000
MAX_FUEL = 100

# Initialize session state variables
if "speed" not in st.session_state:
    st.session_state.speed = 0
if "rpm" not in st.session_state:
    st.session_state.rpm = 0
if "fuel_level" not in st.session_state:
    st.session_state.fuel_level = 100
if "car_status" not in st.session_state:
    st.session_state.car_status = "ON"

# Streamlit Configuration
st.set_page_config(page_title="Futuristic Instrument Cluster", layout="wide")
st.title("Futuristic Instrument Cluster")
st.sidebar.title("Controls")

# Sidebar Controls
st.sidebar.subheader("Car Status")
st.session_state.car_status = st.sidebar.selectbox("Car Status", ["ON", "OFF"])

# Function to update values
def update_values():
    if st.session_state.car_status == "ON":
        st.session_state.speed = (st.session_state.speed + 5) % MAX_SPEED
        st.session_state.rpm = (st.session_state.rpm + 200) % MAX_RPM
        st.session_state.fuel_level = max(0, st.session_state.fuel_level - 1)

# Function to create the instrument cluster
def create_cluster():
    # Create Subplots for Gauges
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "domain", "colspan": 2}, None],  # Speedometer (centered at the top)
               [{"type": "domain"}, {"type": "domain"}]],  # RPM (left) and Fuel (right)
        vertical_spacing=0
    )

    # Speedometer Gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=st.session_state.speed,
            title={"text": "Speed (km/h)", "font": {"size": 18, "color": "white"}},
            gauge={
                "axis": {"range": [0, MAX_SPEED], "tickwidth": 0, "tickcolor": "white"},
                "bar": {"color": "rgba(255, 255, 255, 0)"},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "bordercolor": "white",
                "steps": [
                    {"range": [0, 80], "color": "green"},
                    {"range": [80, 160], "color": "yellow"},
                    {"range": [160, MAX_SPEED], "color": "red"},
                ],
                "threshold": {"line": {"color": "white", "width": 4}, "value": st.session_state.speed},
            },
            number={"font": {"color": "white"}},
        ),
        row=1, col=1
    )

    # RPM Gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=st.session_state.rpm,
            title={"text": "RPM", "font": {"size": 14, "color": "white"}},
            gauge={
                "axis": {"range": [0, MAX_RPM], "tickwidth": 0, "tickcolor": "white"},
                "bar": {"color": "rgba(255, 255, 255, 0)"},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "bordercolor": "white",
                "steps": [
                    {"range": [0, 3000], "color": "green"},
                    {"range": [3000, 6000], "color": "yellow"},
                    {"range": [6000, MAX_RPM], "color": "red"},
                ],
                "threshold": {"line": {"color": "white", "width": 0}, "value": st.session_state.rpm},
            },
            number={"font": {"color": "white"}},
        ),
        row=2, col=1
    )

    # Fuel Gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=st.session_state.fuel_level,
            title={"text": "Fuel (%)", "font": {"size": 14, "color": "white"}},
            gauge={
                "axis": {"range": [0, MAX_FUEL], "tickwidth": 1, "tickcolor": "white"},
                "bar": {"color": "green"},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 2,
                "bordercolor": "white",
            },
            number={"font": {"color": "white"}},
        ),
        row=2, col=2
    )

    # Layout Settings
    fig.update_layout(
        paper_bgcolor="black",
        plot_bgcolor="black",
        height=600,
        margin=dict(t=50, b=20, l=20, r=20),
        font={"color": "white", "family": "Arial"}
    )

    return fig

# Continuously Update the Gauges
placeholder = st.empty()
while True:
    update_values()
    fig = create_cluster()  # Recreate the figure with updated values
    with placeholder.container():
        st.plotly_chart(fig, use_container_width=True)
    time.sleep(1)
