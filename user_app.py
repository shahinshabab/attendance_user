import streamlit as st

# Define the URL of your local server
server_url = 'http://192.168.1.14:5000/'

# Streamlit app layout
st.title('Send HTTP Request with JavaScript')

# HTML and JavaScript embedded in the Streamlit app
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Send Request</title>
</head>
<body>
    <h2>Send HTTP Request</h2>
    <button onclick="sendRequest()">Send Request</button>
    <p id="response"></p>
    
    <script>
        // Define the server URL from the Streamlit app
        const serverUrl = '{server_url}';
        
        // Define the data to send
        const predefinedData = {{
            key1: 'value1',
            key2: 'value2'
        }};
        
        function sendRequest() {{
            // Send the request using Fetch API
            fetch(serverUrl, {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify(predefinedData)
            }})
            .then(response => response.text())
            .then(text => {{
                // Display the response
                document.getElementById('response').innerText = 'Response from server: ' + text;
            }})
            .catch(error => {{
                // Handle errors
                document.getElementById('response').innerText = 'Error: ' + error;
            }});
        }}
    </script>
</body>
</html>
"""


# Render HTML with JavaScript in the Streamlit app
st.markdown(html_code, unsafe_allow_html=True)
