import time
import pandas as pd
import plotly.express as px
import streamlit as st
import os

# Set page to wide mode
st.set_page_config(layout="wide")

# Function to read the CSV file
@st.cache_data(ttl=60)  # Cache for 60 seconds
def get_data() -> pd.DataFrame:
    df = pd.read_csv("output.csv", header=0)  # Read the first row as header
    # Convert numeric columns to float, coercing errors to NaN
    numeric_columns = [col for col in df.columns if col.startswith("Value")]
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
    return df

# Dashboard title
st.title("Real-Time Trade-Data Dashboard")

# Top-level filters
user_filter = st.selectbox("Select User", ["All Users"])  # You can add user filtering if needed

# Create a single-element container
placeholder = st.empty()

# Main loop
while True:
    # Get the latest data
    df = get_data()

    with placeholder.container():
        # Create three columns for KPIs
        kpi1, kpi2, kpi3 = st.columns(3)

        # Fill in the KPIs with the latest data
        latest_data = df.iloc[-1]
        
        def get_metric(column):
            if column in latest_data:
                value = round(float(latest_data[column]), 2)
                delta = round(float(latest_data[column]) - df[column].mean(), 2)
            else:
                value = "N/A"
                delta = None
            return value, delta

        value1, delta1 = get_metric("Value1")
        kpi1.metric(label="Value 1", value=value1, delta=delta1)

        value2, delta2 = get_metric("Value2")
        kpi2.metric(label="Value 2", value=value2, delta=delta2)

        value3, delta3 = get_metric("Value3")
        kpi3.metric(label="Value 3", value=value3, delta=delta3)

        # Create two columns for charts
        fig_col1, fig_col2 = st.columns(2)
        
        with fig_col1:
            st.markdown("### Trade Signal Strength")
            value_columns = [col for col in df.columns if col.startswith("Value")]
            df_melted = df.melt(id_vars=['Timestamp'], 
                                value_vars=value_columns, 
                                var_name='Signal', value_name='Value')
            # Aggregate the data to ensure unique combinations of Signal and Timestamp
            df_aggregated = df_melted.groupby(['Signal', 'Timestamp']).mean().reset_index()
            fig = px.imshow(df_aggregated.pivot(index='Signal', columns='Timestamp', values='Value'),
                            aspect="auto",
                            labels=dict(x="Time", y="Signal", color="Value"),
                            color_continuous_scale='Viridis')
            st.write(fig)
            
        with fig_col2:
            st.markdown("### Value 1 Over Time")
            if "Value1" in df.columns:
                fig2 = px.line(df, x='Timestamp', y='Value1', title='Value 1 Over Time')
                st.write(fig2)
            else:
                st.write("Column 'Value1' not found in the data.")

        st.markdown("### Detailed Data View")
        st.dataframe(df)
        
    # Wait for 60 seconds before the next update
    time.sleep(60)
