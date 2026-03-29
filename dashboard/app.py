import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

import database

WASHING_MACHINE_DEVICE_ID = 1
DRYING_MACHINE_DEVICE_ID = 2

#### APP FUNCTIONS ####
def kpi_bubble(title, is_active):
    color = "#16a34a" if is_active else "#747474"
    status_message = "Active" if is_active else "Inactive"

    return f"""
    <div style="
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 16px;
        background-color: white;
        margin-bottom: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    ">
        <h3 style="margin-bottom: 8px;">{title}</h3>
        <p style="font-size:18px;">
            Current Status: <span style="color:{color};
            font-weight:bold;">{status_message.upper()}</span>
        </p>
    </div>
    """


def get_device_activity_last_6_hours(device_id: int):
    df = database.get_accelerometer_signal_log_data_last_6_hours(
        device_id=device_id
    )
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['timestamp'] = df['timestamp'].dt.tz_localize('UTC')
    df['timestamp'] = df['timestamp'].dt.tz_convert('America/Los_Angeles')

    return df.sort_values(by="timestamp")


def is_device_active(device_id: int):
    activity_df = get_device_activity_last_6_hours(
        device_id=device_id
    )

    if activity_df.empty:
        return False

    last_logged_timestamp = activity_df['timestamp'].max()

    now_pst = pd.Timestamp.now(tz="America/Los_Angeles")

    time_diff = now_pst - last_logged_timestamp

    return time_diff <= pd.Timedelta(minutes=1)


def generate_full_device_activity_last_6_hours(device_id: int):
    activity_df = get_device_activity_last_6_hours(
        device_id=device_id
    )

    now_pst = pd.Timestamp.now(tz="America/Los_Angeles")

    start_pst = now_pst - pd.Timedelta(hours=6)

    # create a range every minute
    time_range = pd.date_range(
        start=start_pst, 
        end=now_pst, 
        freq="1min", 
        tz="America/Los_Angeles"
    )
    time_df = pd.DataFrame({'timestamp': time_range})

    return time_df.join(
        activity_df, 
        how="left", 
        on='timestamp',
        lsuffix='',
        rsuffix='_actual'
    )


### DATA ###
washing_machine_activity_df = generate_full_device_activity_last_6_hours(
    device_id=WASHING_MACHINE_DEVICE_ID
)
drying_machine_activity_df = generate_full_device_activity_last_6_hours(
    device_id=DRYING_MACHINE_DEVICE_ID
)
washing_machine_is_active = is_device_active(
    device_id=WASHING_MACHINE_DEVICE_ID

)
drying_machine_is_active = is_device_active(
    device_id=DRYING_MACHINE_DEVICE_ID
)


#### APP LAYOUT ####
st.set_page_config(
    page_title="Laundry Activity Dashboard",
    page_icon="👕",
    layout="wide",
)
st.title("Laundry Activity Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        kpi_bubble("Washing Machine", washing_machine_is_active),
        unsafe_allow_html=True
    )
    st.subheader("Activity - Last 6 Hours")
    fig = px.line(
        washing_machine_activity_df, 
        x='timestamp', 
        y=['x','y','z'], 
        labels={'value':'Sensor Value','timestamp':'Time'},
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(
        kpi_bubble("Drying Machine", drying_machine_is_active),
        unsafe_allow_html=True
    )
    st.subheader("Activity - Last 6 Hours")
    fig = px.line(
        drying_machine_activity_df, 
        x='timestamp', 
        y=['x','y','z'], 
        labels={'value':'Sensor Value','timestamp':'Time'},
    )
    st.plotly_chart(fig, use_container_width=True)