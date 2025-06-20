import streamlit as st

#Set the page width to wide
st.set_page_config(layout="wide")

# Create tabs
tab1, tab2, tab3 = st.tabs(["EV sale trends", "Charging station growth trends", "EV charging stations map"])

# Content for Tab 1
with tab1:
    st.write("This is the content of Tab 1")
    st.checkbox("Check me in Tab 1")


# Content for Tab 2
with tab2:
    st.write("This is the content of Tab 2")
    st.slider("Slide me in Tab 2", 0, 100, 50)

# Content for Tab 3
with tab3:
 # Display using streamlit-folium
    st.subheader("📍 EV Charging Stations Map")
    st.components.v1.html(open("./output/map.html", "r").read(), height=768, width=1024)
   