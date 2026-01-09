import folium
from streamlit_folium import st_folium

m = folium.Map(
    location=[-7.97, 112.62],
    zoom_start=12,
    tiles="OpenStreetMap"
)

folium.Marker(
    [-7.97, 112.62],
    popup="Test Marker"
).add_to(m)

st_folium(m)
