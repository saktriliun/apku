import streamlit as st
import mysql.connector
from mysql.connector import Error

# Pengaturan tata letak halaman agar elemen tidak melebar ke seluruh layar
st.set_page_config(layout="centered")

# --- INISIALISASI SESSION STATE ---
if "db_connected" not in st.session_state:
    st.session_state.db_connected = False
if "db_config" not in st.session_state:
    st.session_state.db_config = {}

# --- FUNGSI CEK KONEKSI ---
def test_connection(host, user, password, database, port):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            connect_timeout=5
        )
        if conn.is_connected():
            conn.close()
            return True, "Koneksi Berhasil!"
    except Error as e:
        return False, f"Gagal Terhubung: {e}"
    return False, "Gagal Terhubung."

# --- JUDUL HALAMAN ---
st.subheader("⚙️ Pengaturan Koneksi MySQL")
st.write("Masukkan kredensial database MySQL Anda pada formulir di bawah ini:")

# --- MEMBATASI LEBAR FORM (RATA KIRI & TIDAK STRETCH) ---
# Menggunakan 2 kolom: kolom kiri (lebar 2) untuk form, kolom kanan (lebar 1) dibiarkan kosong agar konten rata kiri
col1, col2 = st.columns([2, 1])

with col1:
    # Memasukkan inputan ke dalam komponen Form
    with st.form("connection_form", clear_on_submit=False):
        cfg = st.session_state.db_config
        
        db_host = st.text_input("Database Host", value=cfg.get("host", "localhost"))
        db_port = st.number_input("Port", value=int(cfg.get("port", 3306)), min_value=1, max_value=65535)
        db_user = st.text_input("Username", value=cfg.get("user", "root"))
        db_pass = st.text_input("Password", value=cfg.get("password", ""), type="password")
        db_name = st.text_input("Database Name", value=cfg.get("database", ""))

        # Tombol Submit di dalam Form
        btn_connect = st.form_submit_button("Hubungkan ke Database", type="primary")

    # Logika eksekusi setelah tombol form ditekan
    if btn_connect:
        with st.spinner("Mencoba menghubungkan..."):
            success, message = test_connection(db_host, db_user, db_pass, db_name, db_port)
            
            if success:
                st.session_state.db_connected = True
                st.session_state.db_config = {
                    "host": db_host,
                    "port": db_port,
                    "user": db_user,
                    "password": db_pass,
                    "database": db_name
                }
                st.success(message)
            else:
                st.session_state.db_connected = False
                st.error(message)

    # Indikator Status Koneksi Aktif
    st.markdown("---")
    st.write("Status Koneksi Saat Ini:")
    if st.session_state.db_connected:
        st.success("🟢 TERKONEKSI")
        st.info(f"Terhubung ke database `{st.session_state.db_config.get('database')}`")
    else:
        st.error("🔴 TIDAK TERKONEKSI")
