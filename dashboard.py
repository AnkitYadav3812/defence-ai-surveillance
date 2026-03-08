import streamlit as st
import pandas as pd

st.title("AI Surveillance Monitoring Dashboard")

try:

    data = pd.read_csv("intrusion_log.csv")

    st.subheader("Intrusion Events")

    st.dataframe(data)

    st.metric("Total Intrusions", len(data))

except:

    st.write("No intrusion detected yet")