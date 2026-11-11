import streamlit as st
import requests
import hashlib
from datetime import datetime

# Pengaturan halaman agar rapi di tengah secara bawaan
st.set_page_config(layout="centered", page_title="Aplikasi Antarmuka Utama")

# =============================================================
# KONFIGURASI API SERVER (SESUAI IP & PORT FLASK ANDA)
# =============================================================
API_URL = "http://10.33.73.17:5008/api/secure-post"
SECRET_KEY = "SUPER_SECRET_KEY_ANDA"

def generate_daily_signature(nik):
    today_str = datetime.today().strftime('%Y-%m-%d')
    raw_string = f"{SECRET_KEY}-{today_str}-{nik}"
    return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()

# --- INISIALISASI SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "nama_lengkap" not in st.session_state:
    st.session_state.nama_lengkap = ""
if "username" not in st.session_state:
    st.session_state.username = ""
if "akses" not in st.session_state:
    st.session_state.akses = ""

if not st.session_state.logged_in:
    st.markdown(
        """
        <style>
            [data-testid="stSidebarCollapseButton"] {
                display: none !important;
            }
            [data-testid="stSidebar"] {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- FUNGSI VALIDASI LOGIN VIA API ---
def validate_login(nik, password):
    headers = {
        "Content-Type": "application/json",
        "X-Signature": generate_daily_signature(nik)
    }
    payload = {
        "username": nik,
        "data": {
            "action": "login",
            "password": password
        }
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        
        try:
            res_data = response.json()
        except ValueError:
            st.error(f"❌ Server merespons bukan JSON (Status Code: {response.status_code}).")
            st.code(response.text if response.text else "Respons kosong dari server.")
            return None

        # 1. Jika Login Sukses (flag_status == 1)
        if response.status_code == 200 and res_data.get("status") == "success":
            return res_data.get("user")
            
        # 2. Jika Akun Nonaktif (flag_status == 0)
        elif response.status_code == 403 or res_data.get("status") == "inactive":
            st.warning(f"🚫 **Akses Ditolak:** {res_data.get('message')}")
            st.toast("Akun Anda nonaktif!", icon="🚫")
            return None
            
        # 3. Jika Username/Password Salah atau Error Lainnya
        else:
            st.error(f"❌ {res_data.get('message', 'Login gagal!')}")
            return None

    except requests.exceptions.ConnectionError:
        st.error("❌ Gagal terhubung ke server API. Pastikan server Flask berjalan.")
        return None
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan teknis: {e}")
        return None

# --- FUNGSI LOGOUT VIA API ---
def process_logout(nik):
    headers = {
        "Content-Type": "application/json",
        "X-Signature": generate_daily_signature(nik)
    }
    payload = {
        "username": nik,
        "data": {
            "action": "logout"
        }
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        return response.status_code == 200
    except Exception as e:
        st.warning(f"⚠️ Gagal memperbarui status logout di server: {e}")
        return False


# =============================================================
# KONDISI 1: JIKA USER BERHASIL LOGIN -> HALAMAN UTAMA APLIKASI
# =============================================================
if st.session_state.logged_in:
    st.subheader("📊 APLIKASI LOKET DAN ARSIP DIGITAL")
    st.success(f"👋 Selamat Datang, **{st.session_state.nama_lengkap}**!")
    
    if "confirm_logout" not in st.session_state:
        st.session_state.confirm_logout = False

    if not st.session_state.confirm_logout:
        if st.button("Logout", type="secondary"):
            st.session_state.confirm_logout = True
            st.rerun()
    else:
        st.warning("⚠️ Apakah Anda yakin ingin keluar dari sistem?")    
        col_yes, col_no, col_spacer = st.columns([1, 1, 4])
        with col_yes:
            if st.button("Keluar", type="primary"):
                process_logout(st.session_state.username)
                st.session_state.logged_in = False
                st.session_state.nama_lengkap = ""
                st.session_state.username = ""
                st.session_state.akses = ""
                st.session_state.confirm_logout = False
                st.toast("Anda telah keluar.", icon="ℹ️")
                st.rerun()
                
        with col_no:
            if st.button("Batal", type="secondary"):
                st.session_state.confirm_logout = False
                st.rerun()

    st.markdown("---")
    

# =============================================================
# KONDISI 2: JIKA BELUM LOGIN -> FORM LOGIN DI TENGAH (CENTER)
# =============================================================
else:
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        st.write("")
        st.title("🔐 Login Sistem")
        
        with st.form("login_form", clear_on_submit=False):
            st.subheader("Identifikasi Pengguna")
            input_user = st.text_input("Username")
            input_pass = st.text_input("Password", type="password")
            
            btn_login = st.form_submit_button("Masuk Aplikasi", type="primary")

        if btn_login:
            if not input_user or not input_pass:
                st.warning("Username dan Password wajib diisi!")
            else:
                with st.spinner("Memverifikasi akun Anda..."):
                    user_data = validate_login(input_user.strip(), input_pass)
                    
                    if user_data:
                        st.session_state.logged_in = True
                        st.session_state.nama_lengkap = user_data["nama"]
                        st.session_state.username = user_data["nik"]
                        st.session_state.akses = user_data.get("akses", "")
                        st.toast("Login Berhasil!", icon="✅")
                        st.rerun()
