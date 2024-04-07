import streamlit as st
from Home import face_rec
#import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av

#st.set_page_config(page_title='Registration Form')
 

st.subheader('Registration Form')
registratrion_form = face_rec.RegistrationForm()

person_name = st.text_input(label='Name',placeholder='First & Last Name')
role = st.selectbox(label='Select Role',options=('Student','Teacher'))
def video_callback_func(frame):
    img = frame.to_ndarray(format='bgr24')
    reg_img, embedding = registratrion_form.get_embeddings(img)
    if embedding is not None:
        with open('facial_embeddings.txt',mode='ab') as f:
            np.savetxt(f,embedding)

    return av.VideoFrame.from_ndarray(reg_img,format='bgr24')

webrtc_streamer(key='registration',video_frame_callback=video_callback_func,rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    })

if st.button('Submit'):
    return_val = registratrion_form.save_data(person_name,role)
    if return_val == True:
        st.success(f"{person_name} registered successfully")
    elif return_val == 'name_false':
        st.error('Please enter the name: Name cannot be empty or spaces')
    elif return_val== 'file_false':
        st.error('faial_embeddings.txt is not found!')