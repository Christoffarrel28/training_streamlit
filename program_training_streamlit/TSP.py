'''1. Import Pulp'''
import pulp as lp
from math import radians, cos, sin, asin, sqrt
import pandas as pd

'''2. Haversine '''
def haversine(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))

    return 6371 * c

'''3. Masukkan & Definisikan Permasalahan'''
def tsp(data_kota, nama_kota = None):
    jumlah_kota = len(data_kota)
    kota = []
    if nama_kota is not None:
        kota = nama_kota
    else:
        for i in range(jumlah_kota):
            kota.append(f"Kota-{i+1}")

    jarak = {} 

    for i in range(jumlah_kota):
        for j in range(jumlah_kota):
            kota_asal = kota[i]
            kota_tujuan = kota[j]

            if i == j:
                hasil_jarak = 0
            else:
                hasil_jarak = haversine(data_kota[i], data_kota[j])
            
            jarak[(kota_asal), (kota_tujuan)] = hasil_jarak

    df_jarak = pd.DataFrame(index=kota, columns=kota)

    for (i, j), d in jarak.items():
        df_jarak.loc[i, j] = d

    # df_jarak = df_jarak.astype(int)

    problem = lp.LpProblem("TSP", lp.LpMinimize)

    '''4. Mendefinisikan Variabel Keputusan'''
    rute = lp.LpVariable.dicts('rute', jarak,0,1,lp.LpBinary)
    urutan = lp.LpVariable.dicts('urutan', kota,0,len(kota)-1,lp.LpInteger)

    '''5. Mendefinisikan Fungsi Tujuan'''
    problem += lp.lpSum([jarak[(i,j)] * rute[(i,j)] for i in kota for j in kota if i!=j])

    '''6. Mendefinisikan Batasan/Constraint'''
    for k in kota :
        problem += lp.lpSum([rute[(k,j)] for j in kota if j!=k]) ==1 , f"Ke_{k}"
        problem += lp.lpSum([rute[(i,k)] for i in kota if i!=k]) ==1 , f"Dari_{k}"

    n = len(kota)

    for i in kota :
        for j in kota :
            if i!=j and (i!= kota[0]and j!=kota[0]) :
                problem += urutan[i] - urutan[j] + n* rute[(i,j)] <= n-1

    '''7. Menampilkan Solusi Permasalahan'''
    # problem.writeLP("Permasalahan_TSP")
    status = problem.solve(lp.PULP_CBC_CMD(msg=False))

    rute_map = {}

    for i in kota:
        for j in kota:
            if i != j and lp.value(rute[(i, j)]) == 1:
                rute_map[i] = j    
    
    rute_urut = []
    kota_sekarang =kota[0]

    while True:
        kota_selanjutnya = rute_map[kota_sekarang]
        rute_urut.append((kota_sekarang, kota_selanjutnya))
        kota_sekarang = kota_selanjutnya
        if kota_sekarang == kota[0]:
            break    

    total_jarak =  lp.value(problem.objective)


    return rute_urut, total_jarak, df_jarak