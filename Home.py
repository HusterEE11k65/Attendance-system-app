import streamlit as st
st.set_page_config(page_title='Attendance System',layout = 'wide')
st.header('Attendane System using Face Recognition')
with st.spinner("Loading....."):
    import face_rec
st.success('Loaded successfully')