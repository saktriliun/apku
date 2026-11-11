import streamlit as st
from numpy.random import default_rng as rng

st.subheader(":blue[_Input Loket_] :sunglasses:", divider="rainbow")

with st.form("loket_form"):
   st.write("Data Pemohon")
   my_kec= st.selectbox('Pilih Kecamatan', ['Sidorejo','Tingkir','Argomuylyo','Sidomukti'])
   st.form_submit_button('Simpan')

# This is outside the form
st.write(my_kec)