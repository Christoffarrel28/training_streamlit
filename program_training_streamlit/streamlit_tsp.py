import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium
from TSP import tsp
warna_warni = ["red", 'blue', "green", "purple", "orange", "darkred", "lightred", "beige", "darkblue", "darkgreen", "cadetblue", "darkpurple", "white", "pink", "lightblue", "lightgreen", "gray", "black", "lightgray"]

if "step" not in st.session_state:
    st.session_state.step = 0
if "pin" not in st.session_state:
    st.session_state.pin = []
if "maks_pin" not in st.session_state:
    st.session_state.maks_pin = 0
if "file" not in st.session_state:
    st.session_state.file = None
if "kota" not in st.session_state:
    st.session_state.kota = []

if st.session_state.step == 0:
    
    st.title("Menentukan Rute Optimal dengan TSP")
    st.text("Permasalahan TSP (Traveling Salesman Problem ) adalah permasalahan dimana seorang salesman harus mengunjungi semua kota dimana tiap kota hanya dikunjungi sekali, dan dia harus mulai dari dan kembali ke kota asal. Tujuannya adalah menentukan rute dengan jarak total atau biaya yang paling minimum. ")
    st.subheader("Pilih metode (manual atau Excel)")
    col_man, col_dat = st.columns(2)
    with col_man:
        tombol_manual = st.button("Manual")
        if tombol_manual:
            st.session_state.step = 1
            st.rerun()
    
    with col_dat:
        tombol_file = st.button("Excel")
        if tombol_file:
            st.session_state.step = 4
            st.rerun()    


if st.session_state.step == 1:
    
    st.header("Jumlah Kota")
    st.divider()
    st.session_state.maks_pin = (st.number_input("Masukkan jumlah kota", step= 1, min_value=2))
    tombol_1 = st.button("Selanjutnya")
    if tombol_1:
        st.session_state.step = 2
        st.session_state.pin.clear()
        st.rerun()
    tombol_sekian = st.button("Sebelumnya")
    if tombol_sekian:
        st.session_state.step = 0
        st.rerun()

if st.session_state.step == 2:
    st.title("Pilih Titik Kota Pada Map")
    st.divider()
    if st.session_state.pin == []:
        m = folium.Map(
            location=[-7.983908,112.6280556],
            zoom_start= 14
        )
    else:
        m = folium.Map(
            location= st.session_state.pin[-1],
            zoom_start= 14,
            tiles="OpenStreetMap"
        )

    for i, j in enumerate(st.session_state.pin, start= 1):
        folium.Marker(
            location= j,
            tooltip= folium.Tooltip(f"Kota-{i}", permanent=False, direction="bottom", sticky= False),
            icon=folium.Icon(color=warna_warni[i], icon="city", prefix= "fa")

        ).add_to(m)

    data_kota = st_folium(m, height= 500, width= 500)

    if data_kota["last_clicked"] and len(st.session_state.pin) < st.session_state.maks_pin:
        st.session_state.pin.append(
            [data_kota["last_clicked"]["lat"],
            data_kota["last_clicked"]["lng"]]
        )
        st.rerun()

    col1, col2 = st.columns(2,gap="large")
    with col1:
        tombol_2 = st.button("Sebelumnya")
        if tombol_2:
            st.session_state.step = 1
            st.rerun()
    with col2:
        tombol_3 = st.button("Hitung TSP")
        if tombol_3:
            st.session_state.step = 3
            st.rerun()

if st.session_state.step == 4:
    st.session_state.file = st.file_uploader("Masukkan file excel", type="xlsx")
    if st.session_state.file is not None:
        df_excel = pd.read_excel(st.session_state.file)

        st.session_state.kota = df_excel["Kota"].str.title().dropna().tolist()
        
        st.session_state.pin = df_excel[["latitude", "longitude"]].dropna().astype(float).values.tolist()

    tombol_5 = st.button("Hitung TSP")
    if tombol_5:
        st.session_state.step = 3
        st.rerun()
    tombol_segitu = st.button("Sebelumnya")
    if tombol_segitu:
        st.session_state.step = 0
        st.rerun()

if st.session_state.step == 3:
    st.title("Apa hayo")
    # st.balloons()
    st.divider()
    if st.session_state.kota == []:
        urutan_rute, jarak_total, data_jarak = tsp(st.session_state.pin)
    else:
        urutan_rute, jarak_total, data_jarak = tsp(data_kota=st.session_state.pin, nama_kota= st.session_state.kota)            
    
    m = folium.Map(
        location= st.session_state.pin[0],
        zoom_start= 14,
        tiles="OpenStreetMap"
    )
    kota_index = {}
    if st.session_state.kota == []:
        for i, j in enumerate(st.session_state.pin, start= 1):
            folium.Marker(
                location= j,
                tooltip= folium.Tooltip(f"Kota-{i}", permanent=False, direction="bottom", sticky= False),
                icon=folium.Icon(color=warna_warni[i], icon="city", prefix= "fa")

            ).add_to(m)

        for i in range(len(st.session_state.pin)):
            index_kota = "Kota-" + str(i+1)
            kota_index[index_kota] = i
    else:
        for i, j in enumerate(st.session_state.pin, start= 0):
            folium.Marker(
                location= j,
                tooltip= folium.Tooltip(st.session_state.kota[i], permanent=False, direction="bottom", sticky= False),
                icon=folium.Icon(color=warna_warni[i], icon="city", prefix= "fa")

            ).add_to(m)       
        for i in range(len(st.session_state.pin)):
            index_kota = st.session_state.kota[i]
            kota_index[index_kota] = i

    
    for idx, (i, j) in enumerate(urutan_rute,start=1):
        folium.PolyLine(
            [
                st.session_state.pin[kota_index[i]],
                st.session_state.pin[kota_index[j]]
            ],
            color= warna_warni[idx-7],
            weight=4,
            tooltip=folium.Tooltip(f"Rute ke-{idx}", permanent= True ,direction="top", sticky= False)
            
        ).add_to(m)    

    st.subheader("Jarak Antar Kota")
    st.dataframe(data_jarak)
    st.divider()
    st.subheader("Urutan Rute Optimal")
    col3, col4 = st.columns([10,3])
    with col3:
        st_folium(m, height= 500, width= 500)

    with col4:

        for i, j in urutan_rute:
            st.write(f"{i} → {j}")
    
    st.write(f"Tota jarak adalah {jarak_total:.2f} km")

    tombol_4 = st.button("Selesai")
    if tombol_4:
        st.session_state.step = 0
        st.rerun()




    




    








