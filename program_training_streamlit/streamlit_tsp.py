import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium
from TSP import tsp

colors = [
    "red", 'blue', "green", "purple", "orange", 
    "darkred", "lightred", "beige", "darkblue", "darkgreen", 
    "cadetblue", "darkpurple", "white", "pink", "lightblue", 
    "lightgreen", "gray", "black", "lightgray"
    ]

if "step" not in st.session_state:
    st.session_state.step = 0
if "marker" not in st.session_state:
    st.session_state.marker = []
if "maks_marker" not in st.session_state:
    st.session_state.maks_marker = 0
if "file" not in st.session_state:
    st.session_state.file = None
if "kota" not in st.session_state:
    st.session_state.kota = []
if "hasil_tsp" not in st.session_state:
    st.session_state.hasil_tsp = None

if st.session_state.step == 0:
    st.session_state.kota.clear()
    st.session_state.marker.clear()
    c1 =st.container(border=True)
    with c1:
        st.title("Menentukan Rute Optimal dengan TSP",)
        st.divider()
        st.text(
        "Permasalahan TSP (Traveling Salesman Problem) adalah permasalahan " \
        "dimana seorang salesman harus mengunjungi semua kota dimana tiap " \
        "kota hanya dikunjungi sekali, dan dia harus mulai dari dan kembali " \
        "ke kota asal. Tujuannya adalah menentukan rute dengan jarak total " \
        "atau biaya yang paling minimum. "
        )
        st.subheader("Pilih metode (Manual atau Excel)",text_alignment="center")
        c2 = st.container(horizontal=True, horizontal_alignment="center")
        with c2:
            if st.button("Manual"):
                st.session_state.step = 1
                st.rerun()
            if st.button("Excel"):
                st.session_state.step = 3
                st.rerun()    

if st.session_state.step == 1:
    c3 = st.container(border=True, gap="small")
    with c3:
        st.header("Jumlah Kota")
        st.divider()
        st.session_state.maks_marker = (st.number_input("Masukkan jumlah kota yang diinginkan", min_value=3))

        col_back_1, col_next_1 = st.columns([9,2])
        with col_next_1:
            if st.button("Selanjutnya"):
                st.session_state.step = 2
                st.session_state.marker.clear()
                st.rerun()
        with col_back_1:
            if st.button("Sebelumnya"):
                st.session_state.step = 0
                st.rerun()

@st.cache_data(show_spinner="Menghitung TSP", ttl=60,)
def hitung_tsp_cached(marker, nama_kota=None):
    return tsp(data_kota=marker, nama_kota=nama_kota)

def buat_map(lokasi):
    map = folium.Map(
        location=lokasi,
        zoom_start= 14
    )
    return map

def tambah_marker(index, map, nama_kota=None):
    for i, j in enumerate(st.session_state.marker, start= index):
        folium.Marker(
            location= j,
            tooltip= folium.Tooltip(f"Kota-{i}" if nama_kota is None else nama_kota[i], permanent=False, direction="bottom", sticky= False),
            icon=folium.Icon(color=colors[i], icon="city", prefix= "fa")

        ).add_to(map)  

if st.session_state.step == 2:
    c4 = st.container(border=True)
    with c4:
        st.title("Pilih Titik Kota Pada Map")
        st.divider()
        st.text(f"{len(st.session_state.marker)}/{st.session_state.maks_marker} Kota")

        if st.session_state.marker == []:
            m = buat_map([-7.983908,112.6280556])
        else:
            m = buat_map(st.session_state.marker[-1])

        tambah_marker(1, m)
        
        col_map, col_del = st.columns([3,1])
        with col_map:
            data_kota = st_folium(m, height= 500, width= 500)

        if data_kota["last_clicked"] and len(st.session_state.marker) < st.session_state.maks_marker:
            st.session_state.marker.append(
                [data_kota["last_clicked"]["lat"],
                data_kota["last_clicked"]["lng"]]
            )
            st.rerun()

        with col_del:
            if st.session_state.marker:
                opsi = [f"Kota-{i+1}" for i in range(len(st.session_state.marker))]          
                hapus_kota = st.selectbox("Pilih kota", opsi)
                if st.button("Hapus Kota",width=200):
                    st.session_state.marker.pop(opsi.index(hapus_kota))
                    st.rerun()
            
        col_back_2, col_next_2 = st.columns([6,5],gap="large")
        with col_back_2:
            if st.button("Sebelumnya"):
                st.session_state.step = 1
                st.rerun()

        if len(st.session_state.marker) == st.session_state.maks_marker:
            with col_next_2:
                if st.button("Hitung TSP"):
                    st.session_state.hasil_tsp = hitung_tsp_cached(st.session_state.marker)
                    st.session_state.step = 4
                    st.rerun()

if st.session_state.step == 3:
    c5 = st.container(border=True)
    with c5:
        st.title("File Excel Data Koordinat Kota")
        st.divider()

        st.session_state.file = st.file_uploader("Masukkan file excel", type="xlsx")

        col_back_3, col_next_3 = st.columns(2)
        if st.session_state.file is not None:
            df_excel = pd.read_excel(st.session_state.file)

            st.session_state.kota = df_excel["Kota"].str.title().dropna().tolist()
                
            st.session_state.marker = df_excel[["latitude", "longitude"]].dropna().astype(float).values.tolist()

            with col_next_3:
                if st.button("Hitung TSP"):
                    st.session_state.hasil_tsp = hitung_tsp_cached(st.session_state.marker, st.session_state.kota)
                    st.session_state.step = 4
                    st.rerun()
        
        with col_back_3:
            if st.button("Sebelumnya"):
                st.session_state.step = 0
                st.rerun()

if st.session_state.step == 4:
    c6 = st.container(border=True)
    with c6:
        st.title("Hasil TSP")
        st.divider()

        urutan_rute, jarak_total, data_jarak = st.session_state.hasil_tsp             
        
        m = buat_map(st.session_state.marker[0])
        kota_index = {}
        if st.session_state.kota == []:
            tambah_marker(1, m)

            for i in range(len(st.session_state.marker)):
                index_kota = "Kota-" + str(i+1)
                kota_index[index_kota] = i
        else:
            tambah_marker(0, m, nama_kota=st.session_state.kota)  

            for i in range(len(st.session_state.marker)):
                index_kota = st.session_state.kota[i]
                kota_index[index_kota] = i

        for idx, (i, j) in enumerate(urutan_rute,start=1):
            folium.PolyLine(
                [st.session_state.marker[kota_index[i]],
                    st.session_state.marker[kota_index[j]]],
                color= colors[idx-7],
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

        st.success(f"Tota jarak adalah {jarak_total:.2f} km")

        if st.button("Selesai"):
            st.session_state.step = 0
            st.rerun()
