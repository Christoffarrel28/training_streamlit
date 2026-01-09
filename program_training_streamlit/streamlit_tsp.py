import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("TEST FOLIUM")

m = folium.Map(
    location=[-7.98, 112.63],
    zoom_start=12,
    tiles="OpenStreetMap"
)

folium.Marker(
    [-7.98, 112.63],
    popup="Test Marker"
).add_to(m)

st_folium(m, width=700, height=500)
