import streamlit as st
import os

#Set the page width to wide
st.set_page_config(layout="wide")
# Set the title of the app
st.title("Electric Vehicle (EV) Analysis Dashboard")
# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["EV Trends", "EV registrations By region", "EVs with top range by year and category", "EV charging stations map"])

# Content for Tab 1
with tab1:    
    st.header("Electric Vehicle Model Availability Trends")
    st.caption("Data Sourced from NREL.gov public API ")
    st.image("output/ev_category_trends_linear.png", caption="Electric Models by Type (Last 5 Years)", use_container_width=True)
    st.image("output/ev_seating_capacity_trends_linear.png", caption="Electric Models by Seating Capacity (Last 5 Years)", use_container_width=True)
# Content for Tab 2
with tab2:
    st.header("EV Registrations By State & Climate Region")
    st.caption("Data Sourced from Atlas EV Hub and is limited by the regional availability.")
    st.image('output/top_10_evs_across_states.png',caption="Top Electric Vehicles registrations by state", use_container_width=True)
    st.image("output/top_10_evs_by_region.png", caption="Electric Vehicles registrations by region", use_container_width=True)
    
# Content for Tab 3
with tab3:
    st.header("Top Electric Vehicles by Electric-Only Range")
    st.caption("Data Sourced from NREL.gov public API ")
    st.image("output/evs_by_range_combined.png", use_container_width=True)
 
# Content for Tab 4
with tab4:
    # Display using streamlit-folium
    st.header("📍 EV Charging Stations Map")
    st.caption("Data Sourced from NREL.gov public API ")
    st.components.v1.html(open("./output/map.html", "r").read(), height=768, width=1024)
    
