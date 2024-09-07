import streamlit as st
import requests
import json

st.title('Send JSON Data')

# Input fields for JSON data
key1 = st.text_input('Key 1')
value1 = st.text_input('Value 1')
key2 = st.text_input('Key 2')
value2 = st.text_input('Value 2')

if st.button('Send JSON Request'):
    # Create JSON data
    data = {
        key1: value1,
        key2: value2
    }
    # Replace <your-local-ip>:5000 with your server URL
    url = 'http://192.168.1.14:5000/'
    
    try:
        response = requests.post(url, json=data)
        st.write('Response from server:', response.text)
    except requests.RequestException as e:
        st.error(f'Error: {e}')
