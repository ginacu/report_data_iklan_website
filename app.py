# Libraries 
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import locale
from streamlit_lottie import st_lottie
import requests
from streamlit_lottie import st_lottie_spinner

# Page Behaviour
st.set_page_config(page_title='Report Oktober', page_icon='📊', layout="wide")

# JUDUL
st.title('REPORT BULANAN MP OFC DAN UNOFC - OKTOBER 📊')

# GIF LOTTIE
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raise an exception for error HTTP status codes
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

lottie_url = "https://lottie.host/f4150744-9438-40ab-8766-34fbbac49963/i31N9WisIl.json"
lottie_json = load_lottieurl(lottie_url)

st_lottie(lottie_json, height=270)

st.markdown("""---""")

st.header("🌞 Highlight")

# Remove Default Theme
theme_plotly = None # None or streamlit

# CSS Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


# Load Excel File
df = pd.read_excel('data.xlsx')

def Graphs():
    grafik1, grafik2 = st.columns(2, gap='large') 
    with grafik1:
        grup_team = df.groupby('Team')
        sum_by_team  = grup_team.sum()
        # st.dataframe(sum_by_team)

        # Reset index untuk menjadikan indeks sebagai kolom
        sum_by_team = sum_by_team.reset_index()

        # Pastikan 'Biaya Iklan Total' adalah numerik
        sum_by_team['Biaya Iklan Total'] = pd.to_numeric(sum_by_team['Biaya Iklan Total'], errors='coerce')
        sum_by_team.dropna(subset=['Biaya Iklan Total'], inplace=True)

        # Buat pie chart
        colors = ['#E9E4DF', '#54afaf', '#abbc65', '#94bbb7', '#5ec2cb']

        fig, ax = plt.subplots()
        ax.pie(sum_by_team['Biaya Iklan Total'],
               labels=sum_by_team.Team,
               autopct='%1.1f%%',
               colors=colors)  # Menggunakan Team sebagai label
        ax.set_title('Proporsi Total Biaya Iklan Antar Tim')
        st.pyplot(fig)
    
    with grafik2:
        grup_product = df.groupby('Produk')
        sum_by_product  = grup_product.sum()
        # st.dataframe(sum_by_team)

        # Reset index untuk menjadikan indeks sebagai kolom
        sum_by_product  = sum_by_product.reset_index()

        # Pastikan 'Biaya Iklan Total' adalah numerik
        sum_by_product['Omzet Iklan Total'] = pd.to_numeric(sum_by_product['Omzet Iklan Total'], errors='coerce')
        sum_by_product.dropna(subset=['Omzet Iklan Total'], inplace=True)
        
        # Set format mata uang ke Rupiah
        try:
            locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')  # Gunakan UTF-8
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')  # Fallback ke locale default

        # Urutkan data berdasarkan omzet (descending) dan ambil 5 teratas
        data_top5 = sum_by_product.sort_values('Omzet Iklan Total', ascending=False).head(5)

        # Buat grafik batang
        plt.figure(figsize=(10, 6))
        plt.bar(data_top5['Produk'],
                data_top5['Omzet Iklan Total'],
                color='#37B7C3')
        plt.xlabel('Produk', fontsize=16)
        plt.ylabel('Omzet (Rp)', fontsize=16)
        plt.title('Perbandingan Omzet Penjualan Produk', fontsize=20)

        # Format sumbu y menjadi Rupiah
        plt.gca().yaxis.set_major_formatter(lambda x, pos: locale.currency(x, grouping=True))

        st.pyplot(plt)
    
    st.markdown("""---""")

Graphs()

st.header("🌝 Dashboard")

# Switcher
st.subheader("Masukkan Nama Produk dan Tim untuk Melihat Data Iklan")
produk = st.multiselect(
    "Masukkan nama produk:",
    options = df["Produk"].unique(),
)
team = st.multiselect(
    "Masukkan nama Tim:",
    options = df["Team"].unique(),
)
df_selection = df.query(
    "Produk == @produk & Team == @team"
)

# if team:
#     st.balloons()

# Method / Function
def Keyword():

    # IKLAN KEYWORD
    # 1. Compute Top Analytics
    biaya_iklan_keyword = float(df_selection['Biaya Iklan Keyword'].sum())
    closing_iklan_keyword = float(df_selection['Closing Iklan Keyword'].sum())
    botol_iklan_keyword = float(df_selection['Botol Iklan Keyword'].sum())
    omzet_iklan_keyword = float(df_selection['Omzet Iklan Keyword'].sum())

    # 2. Columns
    total1, total2, total3, total4 = st.columns(4)
    with total1:

        st.info('Biaya Iklan Keyword', icon="🌷")
        st.metric(label=' ', value= f"Rp. {biaya_iklan_keyword:,.0f}")

    with total2:

        st.info('Closing Iklan Keyword', icon="🌸")
        st.metric(label=' ', value= f"{closing_iklan_keyword:,.0f}")

    with total3:

        st.info('Botol Iklan Keyword', icon="🌻")
        st.metric(label=' ', value= f"{botol_iklan_keyword:,.0f}")

    with total4:

        st.info('Omzet Iklan Keyword', icon="🌺")
        st.metric(label=' ', value= f"Rp. {omzet_iklan_keyword:,.0f}")

    st.markdown("""---""")

def Affilliate():

    # IKLAN AFFILIATE
    # 1. Compute Top Analytics
    biaya_iklan_affiliate = float(df_selection['Biaya Iklan Affiliate'].sum())
    closing_iklan_affiliate= float(df_selection['Closing Iklan Affiliate'].sum())
    botol_iklan_affiliate = float(df_selection['Botol Iklan Affiliate'].sum())
    omzet_iklan_affiliate = float(df_selection['Omzet Iklan Affiliate'].sum())

    # 2. Columns
    total1, total2, total3, total4 = st.columns(4) 
    with total1:

        st.info('Biaya Iklan Affiliate', icon="🦊")
        st.metric(label=' ', value= f"Rp. {biaya_iklan_affiliate:,.0f}")

    with total2:

        st.info('Closing Iklan Affiliate', icon="🦧")
        st.metric(label=' ', value= f"{closing_iklan_affiliate:,.0f}")

    with total3:

        st.info('Botol Iklan Affiliate', icon="🦁")
        st.metric(label=' ', value= f"{botol_iklan_affiliate:,.0f}")

    with total4:

        st.info('Omzet Iklan Affiliate', icon="🐯")
        st.metric(label=' ', value= f"Rp. {omzet_iklan_affiliate:,.0f}")

    st.markdown("""---""")

def Cpas():

    # IKLAN CPAS
    # 1. Compute Top Analytics
    biaya_iklan_cpas = float(df_selection['Biaya Iklan CPAS'].sum())
    closing_iklan_cpas = float(df_selection['Closing Iklan CPAS'].sum())
    botol_iklan_cpas = float(df_selection['Botol Iklan CPAS'].sum())
    omzet_iklan_cpas = float(df_selection['Omzet Iklan CPAS'].sum())

    # 2. Columns
    total1, total2, total3, total4 = st.columns(4) 
    with total1:

        st.info('Biaya Iklan CPAS', icon="🌲")
        st.metric(label=' ', value= f"Rp. {biaya_iklan_cpas:,.0f}")

    with total2:

        st.info('Closing Iklan CPAS', icon="🌞")
        st.metric(label=' ', value= f"{closing_iklan_cpas:,.0f}")

    with total3:

        st.info('Botol Iklan CPAS', icon="🍂")
        st.metric(label=' ', value= f"{botol_iklan_cpas:,.0f}")

    with total4:

        st.info('Omzet Iklan CPAS', icon="☃")
        st.metric(label=' ', value= f"Rp. {omzet_iklan_cpas:,.0f}")

    st.markdown("""---""")

def Total():

    # IKLAN TOTAL
    # 1. Compute Top Analytics
    biaya_iklan_total = float(df_selection['Biaya Iklan Total'].sum())
    closing_iklan_total = float(df_selection['Closing Iklan Total'].sum())
    botol_iklan_total = float(df_selection['Botol Iklan Total'].sum())
    omzet_iklan_total = float(df_selection['Omzet Iklan Total'].sum())

    # 2. Columns
    total1, total2, total3, total4 = st.columns(4) 
    with total1:

        st.info('Biaya Iklan Total', icon="🥐")
        st.metric(label=' ', value= f"Rp. {biaya_iklan_total:,.0f}")

    with total2:

        st.info('Closing Iklan Total', icon="🧀")
        st.metric(label=' ', value= f"{closing_iklan_total:,.0f}")

    with total3:

        st.info('Botol Iklan Total', icon="🍕")
        st.metric(label=' ', value= f"{botol_iklan_total:,.0f}")

    with total4:

        st.info('Omzet Iklan Total', icon="🍤")
        st.metric(label=' ', value= f"Rp. {omzet_iklan_total:,.0f}")

    st.markdown("""---""")

def Organik():

    # IKLAN ORGANIK
    # 1. Compute Top Analytics
    biaya_iklan_organik = float(df_selection['Biaya Iklan Organik'].sum())
    closing_iklan_organik = float(df_selection['Closing Iklan Organik'].sum())
    botol_iklan_organik = float(df_selection['Botol Iklan Organik'].sum())
    omzet_iklan_organik = float(df_selection['Omzet Iklan Organik'].sum())

    # 2. Columns
    total1, total2, total3, total4 = st.columns(4) 
    with total1:

        st.info('Biaya Iklan Organik', icon="🗽")
        st.metric(label=' ', value= f"Rp. {biaya_iklan_organik:,.0f}")

    with total2:

        st.info('Closing Iklan Organik', icon="⛲")
        st.metric(label=' ', value= f"{closing_iklan_organik:,.0f}")

    with total3:

        st.info('Botol Iklan Organik', icon="🕋")
        st.metric(label=' ', value= f"{botol_iklan_organik:,.0f}")

    with total4:

        st.info('Omzet Iklan Organik', icon="🗼")
        st.metric(label=' ', value= f"Rp. {omzet_iklan_organik:,.0f}")

    st.markdown("""---""")

st.markdown("""---""")

import streamlit as st

# Inisialisasi status untuk setiap tombol
if 'content_1' not in st.session_state:
    st.session_state.content_1 = False
if 'content_2' not in st.session_state:
    st.session_state.content_2 = False
if 'content_3' not in st.session_state:
    st.session_state.content_3 = False
if 'content_4' not in st.session_state:
    st.session_state.content_4 = False
if 'content_5' not in st.session_state:
    st.session_state.content_5 = False

# Fungsi untuk toggle masing-masing konten
def toggle_content(content_key):
    st.session_state[content_key] = not st.session_state[content_key]

# CONTENT

st.subheader("Data Iklan Toko")
# Tombol untuk menampilkan/menyembunyikan konten
if st.button('Tampilkan Data Iklan Toko'):
    toggle_content('content_1')
# Konten yang akan ditampilkan/ disembunyikan
if st.session_state.content_1:
    Keyword()

st.subheader("Data Iklan Affiliate")
if st.button('Tampilkan Data Iklan Affiliate'):
    toggle_content('content_2')
if st.session_state.content_2:
    Affilliate()

st.subheader("Data Iklan CPAS")
if st.button('Tampilkan Data Iklan CPAS'):
    toggle_content('content_3')
if st.session_state.content_3:
    Cpas()

st.subheader("Data Iklan Organik")
if st.button('Tampilkan Data Iklan Organik'):
    toggle_content('content_4')
if st.session_state.content_4:
    Organik()

st.subheader("Data Iklan Total")
if st.button('Tampilkan Data Iklan Total'):
    toggle_content('content_5')
if st.session_state.content_5:
    Total()


st.header('Tabel Report Bulan Oktober')
st.dataframe(df)