import streamlit as st
from datetime import datetime
import time

def displayTime():
    placeholder = st.empty()
    while True:
        now = datetime.now()
        current_day = now.strftime('%Y/%m/%d')
        current_hour = now.strftime('%H/%H/%S')
        placeholder.markdown(f'{current_day} {current_hour}')
        time.sleep(1)