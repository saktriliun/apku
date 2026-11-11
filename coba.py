import streamlit as st

st.title("Form Grid Multi-Kolom")

# 1. Bungkus seluruh area dengan SATU st.form
with st.form("main_form"):
    st.write("Silahkan isi data di bawah ini:")
    
    # 2. Buat grid menggunakan st.columns di dalam form
    col1, col2, col3 = st.columns(3)
    
    # Baris Pertama
    with col1:
        nama = st.text_input("Nama Lengkap")
    with col2:
        email = st.text_input("Email")
    with col3:
        perusahaan = st.text_input("Perusahaan")
        
    # Baris Kedua (Grid Baru jika diperlukan)
    col4, col5 = st.columns(2)
    with col4:
        opsi = st.selectbox("Pilih Opsi", ["A", "B", "C"])
    with col5:
        jumlah = st.number_input("Jumlah", min_value=1, value=1)
        
    # 3. Satu tombol submit untuk mengirimkan seluruh data grid
    submitted = st.form_submit_button("Kirim Semua Data")

# 4. Proses data setelah tombol ditekan
if submitted:
    st.success("Data berhasil dikirim!")
    st.write({
        "Nama": nama,
        "Email": email,
        "Perusahaan": perusahaan,
        "Opsi": opsi,
        "Jumlah": jumlah
    })
