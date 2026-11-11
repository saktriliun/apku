import streamlit as st


# --- INISIALISASI SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False    
if "nama_lengkap" not in st.session_state:
    st.session_state.nama_lengkap = ""


# =============================================================
# TRIK CSS UNTUK MEMATIKAN SIDEBAR JIKA BELUM LOGGED_IN
# =============================================================
if not st.session_state.logged_in:
    st.markdown(
        """
        <style>
            /* Menyembunyikan tombol navigasi sidebar di pojok kiri atas */
            [data-testid="stSidebarCollapseButton"] {
                display: none !important;
            }
            /* Menyembunyikan bilah sidebar itu sendiri */
            [data-testid="stSidebar"] {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


st.set_page_config(
    page_title="Aplikasi Lokar",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

pages = {
    "Akun": [  # Ini akan menjadi judul kategori pertama
        st.Page("pages/loginku.py", title="Login", icon="🔐"),
    ],    
    "Loket": [  # Ini akan menjadi judul kategori pertama
        st.Page("pages/inputloket.py", title="Input", icon="✏️"),
        st.Page("pages/dataloket.py", title="Data", icon="📋"),
    ],
    "Arsip": [    # Ini akan menjadi judul kategori kedua
        st.Page("pages/uploadarsip.py", title="Upload", icon="📤"),
        st.Page("pages/dataarsip.py", title="Data", icon="🗄️"),
    ],
    "Pengaturan": [    # Ini akan menjadi judul kategori ketiga
            st.Page("pages/koneknya.py", title="Koneksi DB", icon="⚙️"),
        ]
}

# pg = st.navigation(
#     [
#         st.Page(
#             "pages/showcase.py",
#             title="Loket",
#             icon=":material/dashboard:",
#             default=True,
#         ),
#         st.Page("pages/demo_app.py", title="Arsip", icon=":material/menu_book:"),
#         st.Page("pages/examples.py", title="Pengaturan", icon=":material/code:"),
#     ]
# )

pg = st.navigation(pages)
pg.run()

with st.sidebar:
    # st.write(f"👤: :blue[**{st.session_state.nama_lengkap}**!]")
    # st.write("Status Server: Online 🟢")
    if st.session_state.logged_in:
    # st.sidebar.write("  👤 :blue[Angga Pranandaka]")
        # col_stat1, col_stat2 = st.columns(2)
        # with col_stat1 :
        st.write(f"👤 :blue[**{st.session_state.nama_lengkap}**]")
        # col_stat1.metric(label="Status Server", value="Online 🟢")
        # with col_stat2 :
        # st.write("Online 🟢")
    st.caption("Made in :streamlit: by [@saktriliun](https://saktriliun.com)")
    

