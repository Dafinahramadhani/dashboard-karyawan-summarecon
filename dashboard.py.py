#!/usr/bin/env python
# coding: utf-8

# In[148]:


pip install streamlit pandas openpyxl plotly


# In[149]:


import pandas as pd

# Membaca file Excel yang sudah diupload
df = pd.read_excel("file tahunan.xlsx")

# Lihat 5 baris pertama
df.head()


# In[150]:


df.isnull().sum()


# In[151]:


df_cleaned = df.dropna()


# In[152]:


df_cleaned.isnull().sum()


# # Total karyawan

# In[27]:


total_karyawan_akhir = df_akhir['NO. INDUK\n'].nunique()
print(f"Total karyawan aktif di bulan {bulan_terakhir}: {total_karyawan_akhir}")


# In[30]:


import pandas as pd
import plotly.express as px

# 1. Baca data Excel
df = pd.read_excel("file tahunan.xlsx")

# 2. Urutkan bulan agar bisa diproses dengan benar
urutan_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni']
df['Bulan'] = pd.Categorical(df['Bulan'], categories=urutan_bulan, ordered=True)

# 3. Hitung total karyawan unik per bulan
jumlah_per_bulan = df.groupby('Bulan')['NO. INDUK\n'].nunique().reset_index()
jumlah_per_bulan.columns = ['Bulan', 'Jumlah']

# 4. Tampilkan hasil tabel
print("Total jumlah karyawan unik per bulan:")
display(jumlah_per_bulan)

# 5. Visualisasi
fig = px.bar(jumlah_per_bulan,
             x='Bulan', y='Jumlah',
             text='Jumlah',
             title='Jumlah Karyawan per Bulan',
             labels={'Jumlah': 'Jumlah Karyawan'})
fig.update_traces(marker_color='#1ABC9C', textposition='outside')
fig.update_layout(xaxis_title='Bulan', yaxis_title='Jumlah Karyawan')
fig.show()


# In[34]:


import pandas as pd
import plotly.express as px

# 1. Baca data
df = pd.read_excel("file tahunan.xlsx")

# 2. Urutkan bulan
urutan_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni']
df['Bulan'] = pd.Categorical(df['Bulan'], categories=urutan_bulan, ordered=True)

# 3. Normalisasi status
df['STATUS_NORMAL'] = df['STATUS\nKARYAWAN'].apply(
    lambda x: 'Kontrak' if 'KONTRAK' in str(x).upper() else 'Tetap'
)

# 4. Hitung jumlah unik per bulan dan status
jumlah_per_bulan_status = df.groupby(['Bulan', 'STATUS_NORMAL'])['NO. INDUK\n'].nunique().reset_index()
jumlah_per_bulan_status.columns = ['Bulan', 'Status', 'Jumlah']

print("Jumlah karyawan Kontrak & Tetap per bulan:")
display(jumlah_per_bulan_status)

# 5. Visualisasi: line chart dengan marker + text
fig = px.line(
    jumlah_per_bulan_status,
    x='Bulan',
    y='Jumlah',
    color='Status',
    markers=True,
    text='Jumlah',
    title='Jumlah Karyawan Tetap dan Kontrak per Bulan',
    color_discrete_map={
        'Tetap': '#1ABC9C',     
        'Kontrak': '#F39C12'   
    }
)

# 6. Tambahkan gaya dan angka di atas titik
fig.update_traces(textposition='top center', line=dict(width=3), marker=dict(size=10))

# 7. Layout bersih dan profesional
fig.update_layout(
    plot_bgcolor='white',
    xaxis_title='Bulan',
    yaxis_title='Jumlah Karyawan',
    font=dict(family='Segoe UI', size=14),
    title_font_size=20,
    legend_title='Status Karyawan',
    hovermode='x unified'
)

fig.show()


# In[107]:


import pandas as pd
from IPython.display import display, Markdown

# 1. Baca data
df = pd.read_excel("file tahunan.xlsx")

display(Markdown("## 🏢 Tabel Jumlah Karyawan per Unit dan Status Tiap Bulan"))

# 2. Urutkan bulan
urutan_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni']
df['Bulan'] = pd.Categorical(df['Bulan'], categories=urutan_bulan, ordered=True)

# 3. Normalisasi status
df['STATUS_NORMAL'] = df['STATUS\nKARYAWAN'].apply(
    lambda x: 'Kontrak' if 'KONTRAK' in str(x).upper() else 'Tetap'
)

# 4. Hitung jumlah unik per Bulan, Unit, dan Status
jumlah_per_bulan_unit_status = df.groupby(
    ['Bulan', 'NAMA UNIT\n', 'STATUS_NORMAL']
)['NO. INDUK\n'].nunique().reset_index()
jumlah_per_bulan_unit_status.columns = ['Bulan', 'Unit', 'Status', 'Jumlah']

# 5. Buat pivot
pivot_table = jumlah_per_bulan_unit_status.pivot_table(
    index=['Unit', 'Status'],
    columns='Bulan',
    values='Jumlah',
    fill_value=0
)

# 6. Urutkan kolom bulan
pivot_table = pivot_table[urutan_bulan]

# 7. Reset index untuk mengurutkan
pivot_table_reset = pivot_table.reset_index()
pivot_table_reset['Status_order'] = pivot_table_reset['Status'].map({'Tetap': 0, 'Kontrak': 1})
pivot_table_sorted = pivot_table_reset.sort_values(by=['Unit', 'Status_order']).drop(columns='Status_order')
pivot_table_sorted = pivot_table_sorted.set_index(['Unit', 'Status'])

# 8. Tambahkan baris total
total_row = pd.DataFrame(pivot_table_sorted.sum(axis=0)).T
total_row.index = pd.MultiIndex.from_tuples([('TOTAL', '')])
pivot_table_final = pd.concat([pivot_table_sorted, total_row])

# 9. Fungsi pewarnaan
def highlight_status_row(row):
    if row.name[0] == 'TOTAL':
        return ['background-color: black; color: white'] * len(row)
    color_map = {'Tetap': '#1ABC9C', 'Kontrak': '#F39C12'}
    status = row.name[1]
    color = color_map.get(status, '')
    return ['background-color: '+color+'; color: white'] * len(row)

# 10. Tampilkan tabel
styled_pivot = pivot_table_final.style.apply(highlight_status_row, axis=1) \
                                      .set_properties(**{'text-align': 'right'}) \
                                      .format("{:,.0f}")

display(styled_pivot)


# In[105]:


import pandas as pd

# 1. Urutkan bulan
urutan_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni']
df['Bulan'] = pd.Categorical(df['Bulan'], categories=urutan_bulan, ordered=True)

# 2. Normalisasi status
df['STATUS_NORMAL'] = df['STATUS\nKARYAWAN'].apply(
    lambda x: 'Kontrak' if 'KONTRAK' in str(x).upper() else 'Tetap'
)

# 3. Hitung jumlah unik per Bulan, Banding, dan Status
jumlah_per_bulan_banding_status = df.groupby(
    ['Bulan', 'BANDING\n', 'STATUS_NORMAL']
)['NO. INDUK\n'].nunique().reset_index()

jumlah_per_bulan_banding_status.columns = ['Bulan', 'Personal Grade', 'Status', 'Jumlah']

# 4. Buat pivot table: Index = Personal Grade & Status, Kolom = Bulan
pivot_grade_status = jumlah_per_bulan_banding_status.pivot_table(
    index=['Personal Grade', 'Status'],
    columns='Bulan',
    values='Jumlah',
    fill_value=0
)

# 5. Urutkan kolom bulan
pivot_grade_status = pivot_grade_status[urutan_bulan]

# 6. Tambahkan baris total
total_row = pd.DataFrame(pivot_grade_status.sum(axis=0)).T
total_row.index = pd.MultiIndex.from_tuples([('TOTAL', '')])
pivot_grade_status = pd.concat([pivot_grade_status, total_row])

# 7. Fungsi pewarnaan
def highlight_status(row):
    if row.name[0] == 'TOTAL':
        return ['background-color: black; color: white'] * len(row)
    color_map = {'Tetap': '#1ABC9C', 'Kontrak': '#F39C12'}
    status = row.name[1]
    color = color_map.get(status, '')
    return ['background-color: {}; color: white'.format(color)] * len(row)

# 8. Tampilkan tabel
styled_table = pivot_grade_status.style \
    .apply(highlight_status, axis=1) \
    .set_properties(**{'text-align': 'right'}) \
    .format("{:,.0f}")

from IPython.display import display, Markdown
display(Markdown("### 📊 Tabel Jumlah Karyawan per Bulan berdasarkan Personal Grade dan Status "))
display(styled_table)


# In[106]:


import pandas as pd

# 1. Urutkan bulan
urutan_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni']
df['Bulan'] = pd.Categorical(df['Bulan'], categories=urutan_bulan, ordered=True)

# 2. Normalisasi status
df['STATUS_NORMAL'] = df['STATUS\nKARYAWAN'].apply(
    lambda x: 'Kontrak' if 'KONTRAK' in str(x).upper() else 'Tetap'
)

# 3. Normalisasi pendidikan
def normalisasi_pendidikan(p):
    p = str(p).strip().upper()
    if 'S1' in p or 'S-1' in p or 'UNIVERSITAS' in p:
        return 'S1'
    elif 'S2' in p or 'S-2' in p or 'MAGISTER' in p:
        return 'S2'
    elif 'S3' in p or 'S-3' in p or 'DOKTOR' in p:
        return 'S3'
    elif 'D3' in p or 'D III' in p or 'AKADEMI' in p:
        return 'D3'
    elif 'D2' in p or 'D II' in p:
        return 'D2'
    elif 'D1' in p or 'D I' in p:
        return 'D1'
    elif any(x in p for x in ['SMK', 'SLTA', 'SMA', 'SMU', 'STM']):
        return 'SLTA'
    elif 'SMP' in p:
        return 'SMP'
    elif 'SD' in p:
        return 'SD'
    else:
        return 'LAINNYA'

df['PENDIDIKAN_NORMAL'] = df['PENDIDIKAN\n'].apply(normalisasi_pendidikan)

# 4. Hitung jumlah unik per Bulan, Pendidikan, dan Status
jumlah_per_bulan_pendidikan_status = df.groupby(['Bulan', 'PENDIDIKAN_NORMAL', 'STATUS_NORMAL'])['NO. INDUK\n'].nunique().reset_index()
jumlah_per_bulan_pendidikan_status.columns = ['Bulan', 'Pendidikan', 'Status', 'Jumlah']

# 5. Buat pivot table
pivot_pendidikan_status = jumlah_per_bulan_pendidikan_status.pivot_table(
    index=['Pendidikan', 'Status'],
    columns='Bulan',
    values='Jumlah',
    fill_value=0
)

# 6. Tambahkan baris total
total_row = pd.DataFrame(pivot_pendidikan_status.sum(axis=0)).T
total_row.index = pd.MultiIndex.from_tuples([('TOTAL', '')])  # buat baris index gabungan
pivot_pendidikan_status = pd.concat([pivot_pendidikan_status, total_row])

# 7. Urutkan kolom sesuai bulan
pivot_pendidikan_status = pivot_pendidikan_status[urutan_bulan]

# 8. Fungsi pewarnaan baris berdasarkan status
def highlight_status(row):
    if row.name[0] == 'TOTAL':
        return ['background-color: black; color: white'] * len(row)
    color_map = {'Tetap': '#1ABC9C', 'Kontrak': '#F39C12'}  # Hijau toska & Oranye
    status = row.name[1]
    color = color_map.get(status, '')
    return ['background-color: {}; color: white'.format(color)] * len(row)

# 9. Tampilkan tabel dengan format dan warna
styled_table = pivot_pendidikan_status.style \
    .apply(highlight_status, axis=1) \
    .set_properties(**{'text-align': 'right'}) \
    .format("{:,.0f}") \

from IPython.display import display, Markdown
display(Markdown("### 🎓 Tabel Jumlah Karyawan per Bulan berdasarkan Jenis Pendidikan dan Status "))
display(styled_table)


# In[108]:


import pandas as pd
from IPython.display import display, Markdown

# 1. Urutkan bulan
urutan_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni']
df['Bulan'] = pd.Categorical(df['Bulan'], categories=urutan_bulan, ordered=True)

# 2. Normalisasi jenis kelamin
df['SEX_NORM'] = df['SEX\n'].apply(lambda x: 'Laki-laki' if str(x).strip().upper() in ['L', 'LAKI-LAKI'] else 'Perempuan')

# 3. Hitung jumlah karyawan unik per bulan dan jenis kelamin
jumlah_per_bulan_sex = df.groupby(['Bulan', 'SEX_NORM'])['NO. INDUK\n'].nunique().reset_index()
jumlah_per_bulan_sex.columns = ['Bulan', 'Jenis Kelamin', 'Jumlah']

# 4. Buat pivot table: index = Jenis Kelamin, kolom = Bulan
pivot_sex = jumlah_per_bulan_sex.pivot_table(
    index='Jenis Kelamin',
    columns='Bulan',
    values='Jumlah',
    fill_value=0
)

# 5. Urutkan kolom bulan
pivot_sex = pivot_sex[urutan_bulan]

# 6. Tambahkan baris total
total_row = pd.DataFrame(pivot_sex.sum(axis=0)).T
total_row.index = ['TOTAL']
pivot_sex_final = pd.concat([pivot_sex, total_row])

# 7. Fungsi pewarnaan
def highlight_sex(row):
    if row.name == 'Laki-laki':
        return ['background-color: #3498DB; color: white'] * len(row)  # Biru
    elif row.name == 'Perempuan':
        return ['background-color: #E91E63; color: white'] * len(row)  # Pink
    elif row.name == 'TOTAL':
        return ['background-color: black; color: white'] * len(row)
    else:
        return [''] * len(row)

# 8. Tampilkan
styled_sex = pivot_sex_final.style.apply(highlight_sex, axis=1) \
                                  .set_properties(**{'text-align': 'right'}) \
                                  .format("{:,.0f}")

display(Markdown("### 👥 Tabel Jumlah Karyawan per Bulan berdasarkan Jenis Kelamin"))
display(styled_sex)


# In[139]:


import pandas as pd
import plotly.graph_objects as go

# 1. Normalisasi Jenis Kelamin
df['SEX_NORM'] = df['SEX\n'].apply(lambda x: 'Laki-laki' if str(x).strip().upper() in ['L', 'LAKI-LAKI'] else 'Perempuan')

# 2. Normalisasi Status
df['STATUS_NORMAL'] = df['STATUS\nKARYAWAN'].apply(lambda x: 'Kontrak' if 'KONTRAK' in str(x).upper() else 'Tetap')

# 3. Urutkan Bulan
urutan_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni']
df['Bulan'] = pd.Categorical(df['Bulan'], categories=urutan_bulan, ordered=True)

# 4. Hitung jumlah unik per Bulan, Jenis Kelamin, dan Status
grouped = df.groupby(['Bulan', 'SEX_NORM', 'STATUS_NORMAL'])['NO. INDUK\n'].nunique().reset_index()
pivot = grouped.pivot_table(index='Bulan', columns=['SEX_NORM', 'STATUS_NORMAL'], values='NO. INDUK\n', fill_value=0)

# 5. Buat grafik batang interaktif
fig = go.Figure()

color_map = {
    ('Laki-laki', 'Tetap'): '#2980B9',     # Biru tua
    ('Laki-laki', 'Kontrak'): '#85C1E9',  # Biru muda
    ('Perempuan', 'Tetap'): '#E91E63',    # Pink tua
    ('Perempuan', 'Kontrak'): '#F1948A'   # Pink muda
}

# Tambahkan bar per kombinasi jenis kelamin & status
for (jk, st), color in color_map.items():
    fig.add_trace(go.Bar(
        x=pivot.index,
        y=pivot[(jk, st)],
        name=f"{jk} - {st}",
        marker_color=color,
        text=pivot[(jk, st)],
        textposition='inside',
        hovertemplate=f'{jk} - {st}<br>Bulan: %{{x}}<br>Jumlah: %{{y}}<extra></extra>',
    ))

# 6. Hitung total
total_semua = pivot.sum(axis=1)
total_laki = pivot.xs('Laki-laki', level=0, axis=1).sum(axis=1)
total_perempuan = pivot.xs('Perempuan', level=0, axis=1).sum(axis=1)

# Tambahkan teks Total, Perempuan, Laki-laki (urutan atas ke bawah)
for bulan in pivot.index:
    # Total (paling atas)
    fig.add_trace(go.Scatter(
        x=[bulan],
        y=[total_semua[bulan] + 35],
        text=[f"<b>Total: {total_semua[bulan]}</b>"],
        mode='text',
        textfont=dict(size=13, color='black', family='Arial Black'),
        showlegend=False
    ))

    # Perempuan
    fig.add_trace(go.Scatter(
        x=[bulan],
        y=[total_semua[bulan] + 20],
        text=[f"<b>Perempuan: {total_perempuan[bulan]}</b>"],
        mode='text',
        textfont=dict(size=11, color='#E91E63', family='Arial Black'),
        showlegend=False
    ))

    # Laki-laki
    fig.add_trace(go.Scatter(
        x=[bulan],
        y=[total_semua[bulan] + 5],
        text=[f"<b>Laki-laki: {total_laki[bulan]}</b>"],
        mode='text',
        textfont=dict(size=11, color='#2980B9', family='Arial Black'),
        showlegend=False
    ))

# 7. Layout & Tampilan
fig.update_layout(
    title="📊 Distribusi Karyawan per Bulan berdasarkan Jenis Kelamin dan Status",
    xaxis_title="Bulan",
    yaxis_title="Jumlah Karyawan",
    barmode='stack',
    height=550,
    width=1100,
    legend_title="Keterangan",
    margin=dict(t=100, b=40, l=50, r=50),
)

fig.show()


# In[173]:


import pandas as pd
import plotly.express as px

# --- 1. Bersihkan nama kolom ---
df.columns = df.columns.str.strip().str.replace('\n', ' ')  # contoh: 'TANGGAL LAHIR' tetap dikenali

# --- 2. Ubah ke datetime & ambil tahun lahir ---
df['TANGGAL LAHIR'] = pd.to_datetime(df['TANGGAL LAHIR'], errors='coerce')
df['TahunLahir'] = df['TANGGAL LAHIR'].dt.year

# --- 3. Buat kolom generasi berdasarkan tahun lahir ---
def tentukan_generasi(tahun):
    if pd.isnull(tahun):
        return 'Tidak Diketahui'
    elif tahun <= 1964:
        return 'Baby Boomer'
    elif tahun <= 1980:
        return 'Gen X'
    elif tahun <= 1996:
        return 'Millennial'
    elif tahun <= 2012:
        return 'Gen Z'
    else:
        return 'Gen Alpha'

df['Generasi'] = df['TahunLahir'].apply(tentukan_generasi)
# --- 4. Urutkan bulan ---
urutan_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni']
df['Bulan'] = pd.Categorical(df['Bulan'], categories=urutan_bulan, ordered=True)

# --- 5. Hitung jumlah karyawan unik per bulan dan generasi ---
grouped = df.groupby(['Bulan', 'Generasi'])['NO. INDUK'].nunique().reset_index(name='Jumlah')

# --- 6. Warna sesuai permintaan ---
color_custom = {
    'Baby Boomer': '#B2BABB',     # Abu-abu
    'Gen X': '#76D7C4',           # Biru muda
    'Millennial': '#F9E79F',      # Merah muda
    'Gen Z': '#85C1E9',           # Pastel ungu
    'Gen Alpha': '#F9E79F',       # Kuning pastel
    'Tidak Diketahui': '#D5DBDB'  # Abu muda
}

# --- 7. Buat grafik batang interaktif ---
fig = px.bar(
    grouped,
    x='Bulan',
    y='Jumlah',
    color='Generasi',
    text='Jumlah',
    barmode='stack',
    color_discrete_map=color_custom,
    category_orders={
        'Bulan': urutan_bulan,
        'Generasi': ['Baby Boomer', 'Gen X', 'Millennial', 'Gen Z', 'Gen Alpha', 'Tidak Diketahui']
    },
    title="📊 Distribusi Karyawan Berdasarkan Generasi per Bulan"
)

# --- 8. Tampilan layout ---
fig.update_traces(
    textposition='inside',
    textfont=dict(size=11, family='Arial')
)
fig.update_layout(
    xaxis_title="Bulan",
    yaxis_title="Jumlah Karyawan",
    height=550,
    width=1100,
    legend_title="Generasi",
    margin=dict(t=80, b=40, l=50, r=50),
    plot_bgcolor='white'
)

fig.show()


# In[179]:


import pandas as pd
import plotly.express as px

# --- 1. Bersihkan nama kolom ---
df.columns = df.columns.str.strip().str.replace('\n', ' ')

# --- 2. Ubah ke datetime & ambil tahun lahir ---
df['TANGGAL LAHIR'] = pd.to_datetime(df['TANGGAL LAHIR'], errors='coerce')
df['TahunLahir'] = df['TANGGAL LAHIR'].dt.year

# --- 3. Buat kolom generasi ---
def tentukan_generasi(tahun):
    if pd.isnull(tahun):
        return 'Tidak Diketahui'
    elif tahun <= 1964:
        return 'Baby Boomer'
    elif tahun <= 1980:
        return 'Gen X'
    elif tahun <= 1996:
        return 'Millennial'
    elif tahun <= 2012:
        return 'Gen Z'
    else:
        return 'Gen Alpha'

df['Generasi'] = df['TahunLahir'].apply(tentukan_generasi)

# --- 4. Normalisasi Status Karyawan ---
df['STATUS_NORMAL'] = df['STATUS KARYAWAN'].apply(
    lambda x: 'Kontrak' if 'KONTRAK' in str(x).upper() else 'Tetap'
)

# --- 5. Urutkan Bulan & Generasi ---
urutan_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni']
urutan_generasi = ['Baby Boomer', 'Gen X', 'Millennial', 'Gen Z', 'Gen Alpha', 'Tidak Diketahui']
df['Bulan'] = pd.Categorical(df['Bulan'], categories=urutan_bulan, ordered=True)
df['Generasi'] = pd.Categorical(df['Generasi'], categories=urutan_generasi, ordered=True)

df['Kelompok'] = df['Generasi'].astype(str) + ' - ' + df['STATUS_NORMAL'].astype(str)


# --- 7. Hitung jumlah karyawan per Bulan & Kelompok ---
grouped = df.groupby(['Bulan', 'Kelompok'])['NO. INDUK'].nunique().reset_index(name='Jumlah')

# --- 8. Warna khusus untuk kombinasi Generasi + Status ---
color_custom = {
    'Baby Boomer - Tetap': '#808B96',      # Abu tua
    'Baby Boomer - Kontrak': '#D5D8DC',    # Abu muda
    'Gen X - Tetap': '#48C9B0',            # Tosca tua
    'Gen X - Kontrak': '#A3E4D7',          # Tosca muda
    'Millennial - Tetap': '#F1948A',       # Pink coral
    'Millennial - Kontrak': '#FADBD8',     # Pink muda
    'Gen Z - Tetap': '#5DADE2',            # Biru lembut
    'Gen Z - Kontrak': '#D6EAF8',          # Biru pastel
    'Gen Alpha - Tetap': '#F8C471',        # Orange pastel
    'Gen Alpha - Kontrak': '#FEF5E7',      # Kuning muda
    'Tidak Diketahui - Tetap': '#B2BABB',
    'Tidak Diketahui - Kontrak': '#E5E8E8'
}

# --- 9. Buat diagram batang gabungan ---
fig = px.bar(
    grouped,
    x='Bulan',
    y='Jumlah',
    color='Kelompok',
    text='Jumlah',
    barmode='stack',
    color_discrete_map=color_custom,
    category_orders={
        'Bulan': urutan_bulan,
        'Kelompok': list(color_custom.keys())  # agar urutan sesuai
    },
    title="📊 Distribusi Karyawan Tetap & Kontrak Berdasarkan Generasi per Bulan"
)

# --- 10. Tampilan layout ---
fig.update_traces(
    textposition='inside',
    textfont=dict(size=11, family='Arial')
)
fig.update_layout(
    xaxis_title="Bulan",
    yaxis_title="Jumlah Karyawan",
    height=600,
    width=1150,
    legend_title="Generasi - Status",
    margin=dict(t=80, b=40, l=50, r=50),
    plot_bgcolor='white'
)

fig.show()


# In[181]:


df.to_csv("data_karyawan_bersih.csv", index=False)


# In[ ]:




