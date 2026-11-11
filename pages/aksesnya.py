import streamlit as st
import requests
import hashlib
from datetime import datetime

# Konfigurasi Target API (Pastikan port dan IP sesuai dengan Flask Anda)
API_URL = "http://10.33.73.17:5008/api/secure-post"
SECRET_KEY = "SUPER_SECRET_KEY_ANDA"

st.set_page_config(page_title="Client API Secure", page_icon="🔐")
st.title("🔐 Pengiriman Data Secure API")
st.markdown("Aplikasi client ini otomatis menghasilkan token **SHA-256** harian berdasarkan kombinasi `SECRET_KEY`, tanggal hari ini, dan `NIK`.")

# Form Input Streamlit
with st.form("form_kirim_data"):
    nik_input = st.text_input("NIK Pengguna", value="3324072907880003")
    judul_data = st.text_input("Judul / Kategori Laporan", value="Laporan Harian")
    isi_pesan = st.text_area("Detail Data / Catatan", value="Data berhasil dikirim dari antarmuka Streamlit.")
    
    submit_btn = st.form_submit_button("Mohon Tunggu Kirim Data ke Server")

if submit_btn:
    if not nik_input.strip():
        st.error("NIK tidak boleh kosong!")
    else:
        with st.spinner("Menghitung signature dan menghubungi server..."):
            # 1. Buat Signature Harian Otomatis
            today_str = datetime.today().strftime('%Y-%m-%d')
            raw_string = f"{SECRET_KEY}-{today_str}-{nik_input.strip()}"
            generated_signature = hashlib.sha256(raw_string.encode('utf-8')).hexdigest()

            # 2. Susun Payload JSON & Headers
            payload = {
                "username": nik_input.strip(),
                "data": {
                    "judul": judul_data,
                    "catatan": isi_pesan,
                    "waktu_kirim": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "X-Signature": generated_signature
            }

            # 3. Kirim POST Request ke Server Flask
            try:
                response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
                res_json = response.json()

                if response.status_code == 200:
                    nama_user = res_json.get('user', {}).get('nama', 'Pengguna')
                    st.success(f"Berhasil! Data diproses untuk **{nama_user}**.")
                    with st.expander("Lihat Detail Respons Server & Token"):
                        st.write(f"**Signature Terkirim:** `{generated_signature}`")
                        st.json(res_json)
                elif response.status_code == 403:
                    st.warning(f"Akses Ditolak: {res_json.get('message')}")
                elif response.status_code == 401:
                    st.error(f"Autentikasi Gagal: {res_json.get('message')}")
                else:
                    st.error(f"Error ({response.status_code}): {res_json.get('message')}")

            except requests.exceptions.ConnectionError:
                st.error("Gagal terhubung ke server Flask. Pastikan file `app.py` sudah dijalankan.")
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")
