import streamlit as st
import folium
from streamlit_folium import st_folium

m = folium.Map(
    location=[-7.98, 112.63],
    zoom_start=14,
    tiles="OpenStreetMap"
)

folium.Marker(
    [-7.98, 112.63],
    popup="Test"
).add_to(m)

st_folium(m)
