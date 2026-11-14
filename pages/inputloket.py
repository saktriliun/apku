import streamlit as st
from numpy.random import default_rng as rng

st.subheader(":blue[_Input Loket_] :sunglasses:", divider="rainbow")

with st.form("loket_form"):
   st.write("Data Pemohon")
   input_nikpemohon = st.text_input("NIK Pemohon")
   input_namapemohon = st.text_input("Nama Pemohon")
   input_namakec= st.selectbox('Pilih Kecamatan', ['Sidorejo','Tingkir','Argomuylyo','Sidomukti'])
   input_namakel= st.selectbox('Pilih Kelurahan', ['Sidorejo','Tingkir','Argomuylyo','Sidomukti'])
   input_nohppemohon = st.text_input("Nomor HP")
   input_emailpemohon = st.text_input("Email Pemohon")

   agree = st.checkbox("Pelapor adalah Pemohon")
   if agree:
      st.text_input(input_nikpemohon)

   input_nikpelapor = st.text_input("NIK Pelapor")
   input_namapelapor = st.text_input("Nama Pelapor")
   st.form_submit_button('Simpan')

# This is outside the form
st.write(input_namakec)
st.write(input_namakel)