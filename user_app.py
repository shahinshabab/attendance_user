import streamlit as st
import requests

def send_request():
    try:
        # Replace <your-local-ip> with the IP address of your local server
        response = requests.get('http://192.168.1.14:5000/')
        return response.text
    except requests.RequestException as e:
        return f'Error: {e}'

st.title('Streamlit HTTP Request Example')

if st.button('Send Request'):
    result = send_request()
    st.write(result)
