import streamlit as st
from Home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time

#st.set_page_config(page_title='Real Time Prediction')

st.subheader('Real-Time Attendance System')

# Retrive the data from Redis Database
with st.spinner('Retriving data....'):
    redis_face_db = face_rec.retrive_data(name = 'Dolphin:Register')
    st.dataframe(redis_face_db)
st.success('Successfully')
waitTime = 30
setTime = time.time()
realtimepred = face_rec.RealTimePred()

# Real Time prediction
# strealit webrtc

def video_frame_callback(frame):
    global setTime
    img = frame.to_ndarray(format="bgr24")
    pred_img = realtimepred.face_prediction(img,redis_face_db,'facial_features',['Name','Role'],thresh = 0.5)
    timenow= time.time()
    difftime = timenow - setTime
    if difftime >= waitTime:
        realtimepred.saveLogs()
        setTime= time.time()
        print('Saved data to redis')
    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")


webrtc_streamer(key="example", video_frame_callback=video_frame_callback,rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    })