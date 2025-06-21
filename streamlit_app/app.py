import streamlit as st
import os

#Set the page width to wide
st.set_page_config(layout="wide")
# Set the title of the app
st.title("Electric Vehicle (EV) Viability Dashboard")
# Create tabs
tab1, tab2, tab3 = st.tabs(["EVs with top range by year and category", "Charging station growth trends", "EV charging stations map"])

# Content for Tab 1
with tab1:    
    st.subheader("Top Electric Vehicles by Electric-Only Range")
    st.write("This section displays the top electric vehicles by electric-only range for the last 4 years, categorized by model and manufacturer.")
    st.image("output/evs_by_range_combined.png", caption="Top Electric Vehicles by Electric-Only Range (Last 3 Years)", use_container_width=True)

# Content for Tab 2
with tab2:
    st.write("This is the content of Tab 2")
    st.slider("Slide me in Tab 2", 0, 100, 50)

# Content for Tab 3
with tab3:
 # Display using streamlit-folium
    st.subheader("📍 EV Charging Stations Map")
    st.components.v1.html(open("./output/map.html", "r").read(), height=768, width=1024)
   