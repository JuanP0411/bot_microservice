import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import random
from datetime import datetime, timedelta


def add_rows(df, user, n):
    """
    Adds n rows to the DataFrame for the specified user with incrementing timestamps.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to which rows will be added.
    user (str): The user for whom to add rows.
    n (int): The number of rows to add.
    
    Returns:
    pd.DataFrame: The updated DataFrame.
    """
    # Get the last timestamp in the DataFrame and convert to datetime
    last_timestamp = pd.to_datetime(df['Timestamp'].iloc[-1])
    new_rows = []
    for i in range(n):
        # Increment the timestamp by 1 minute
        new_timestamp = last_timestamp + timedelta(minutes=i + 1)
        
        # Generate random values for the new row
        new_row = {
            'User': user,
            'Test3': round(random.uniform(170, 200), 2),
            'Signal1': round(random.uniform(160, 175), 2),
            'Signal2': round(random.uniform(175, 185), 2),
            'Signal4': round(random.uniform(165, 170), 2),
            'Signal5': round(random.uniform(150, 176), 2),
            'Signal6': round(random.uniform(180, 200), 2),
            'Signal7': round(random.uniform(190, 210), 2),
            'Signal8': round(random.uniform(160, 180), 2),
            'Timestamp': new_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'TradeValue': round(random.uniform(150, 170), 2),
            'order': random.choice(['buy', 'sell'])
        }
        new_rows.append(new_row)
    
    # Create a DataFrame from the list of new rows
    new_df = pd.DataFrame(new_rows)
    df = df.drop(df.index[0])
    
    # Concatenate the original DataFrame with the new rows DataFrame
    df = pd.concat([df, new_df], ignore_index=True)
    
    return df






st.set_page_config(
    page_title="Real-Time Trade-Data Dashboard",
    page_icon="✅",
    layout="wide",
)
#crear un envionrment para correr esto
# read csv from a github repo
dataset_url = "Test_data_trading.csv"

# read csv from a URL
@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

graph_dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

@st.cache_data
def get_data_graph() -> pd.DataFrame:
    return pd.read_csv(graph_dataset_url)

df = get_data()

df_graphs = get_data_graph()

# dashboard title
st.title("Real-Time / Trade-Data Dashboard")

# top-level filters
job_filter = st.selectbox("Select User", pd.unique(df["User"]))

# creating a single-element container
placeholder = st.empty()

# dataframe filter
df = df[df["User"] == job_filter]
count_married= len(df) 
df_length = len(df)
# near real-time / live feed simulation
for seconds in range(2000000000000000000000):
    df = add_rows(df,job_filter,1)
    df_graphs["age_new"] = df_graphs["age"] * np.random.choice(range(1, 5))
    avg_age = np.mean(df_graphs["age_new"])





    random_data = np.random.choice(range(-2, 2))
    random_data2 = np.random.choice(range(-2, 2))
    df["Test3_new"] = df["Test3"] * np.random.choice(range(1, 5))
    df["Signal1_new"] = df["Signal1"] * np.random.choice(range(1, 5))
    df["TradeValue_new"] = df["TradeValue"] + random_data
    df["TradeValue_new_volatile"] = df["TradeValue_new"] + np.random.choice(range(-20, 20))
    # creating KPIs
    df["NEGATIVE"] = df["TradeValue_new"]* -1
    avg_age = np.mean(df["TradeValue_new"])

    choice = np.random.choice(range(-10, 10))
    
    if(choice >= 7):
     count_married += 1
 
    buy_count = (df['order'] == 'buy').sum() + random_data
    sell_count = (df['order'] == 'sell').sum() + random_data2

# Calculate the ratio of buy to sell
    buy_sell_ratio = buy_count / sell_count if sell_count != 0 else 'Cannot divide by zero'
    balance = np.mean(df["TradeValue_new"])
    ganancia_perdida_trans = balance/df_length

    with placeholder.container():

        # create three columns
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="Ganancia perdida por transaccion",
            value=round(ganancia_perdida_trans,2),
            delta=round(ganancia_perdida_trans,2) - 10,
        )
        
        kpi2.metric(
            label="Numero de Transacciones ",
            value=int(count_married),
            delta=-10 + count_married,
        )
        
        kpi3.metric(
            label="Ganancia perdida＄",
            value=f"$ {round(balance,2)} ",
            delta=- int(random_data),
        )



        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        # Melt the DataFrame to have a long format suitable for heatmap
        df_melted = df.melt(id_vars=['Timestamp'], value_vars=['Test3','Signal1', 'Signal2', 'Signal4', 'Signal5','Signal6', 'Signal7', 'Signal8'], 
                    var_name='Signal', value_name='Value')

        # create two columns for charts

        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### Trade Signal Strength")
            fig = px.imshow(df_melted.pivot(index='Signal', columns='Timestamp', values='Value'), 
                aspect="auto", 
                labels=dict(x="Time", y="Signal", color="Value"),
                color_continuous_scale='Viridis')

            st.write(fig)
            
        with fig_col2:

            fig_col1_1 = st.container()
            with fig_col1_1:
                st.markdown("### historico compra")
                fig4 = px.bar(df, x='Timestamp', y='TradeValue_new_volatile')
                fig4.update_layout(
                        width=500,  # Set the width of the plot
                        height=300  # Set the height of the plot
                        )
                fig4.update_yaxes(title_text='Valor de Compra')
                st.write(fig4)

            
                st.markdown("### historico venta")
                fig3 = px.bar(df, x='Timestamp', y='NEGATIVE',color_discrete_sequence=['#FF7F7F'])
                fig3.update_layout(
                        width=500,  # Set the width of the plot
                        height=300  # Set the height of the plot
                        )
                fig3.update_yaxes(title_text='Valor de Venta')
                st.write(fig3)

            

        st.markdown("### Detailed Data View")
        st.dataframe(df.iloc[:, :12])
        time.sleep(1)


