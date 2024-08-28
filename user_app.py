import streamlit as st
import pandas as pd
import time

# Define the HTML and JavaScript code
html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>Local IP Detection</title>
</head>
<body>
    <h1>Local IP Detection</h1>
    <div id="local-ip">Detecting...</div>
    <script>
        function getLocalIPs() {
            var ips = [];
            var pc = new RTCPeerConnection({iceServers: []});
            pc.createDataChannel('');
            
            pc.createOffer().then(function(sdp) {
                return pc.setLocalDescription(sdp);
            }).catch(function(error) {
                console.error('Error creating offer:', error);
            });

            pc.onicecandidate = function(event) {
                if (event.candidate) {
                    var ip = /([0-9]{1,3}\.){3}[0-9]{1,3}/.exec(event.candidate.candidate);
                    if (ip) {
                        ips.push(ip[0]);
                        document.getElementById('local-ip').innerText = 'Local IP Addresses: ' + ips.join(', ');
                        
                        // Send IPs to Streamlit using a hidden form
                        var xhr = new XMLHttpRequest();
                        xhr.open('POST', '/update_ips', true);
                        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                        xhr.send('ips=' + encodeURIComponent(ips.join(',')));
                    }
                }
            };

            setTimeout(() => {
                if (ips.length === 0) {
                    document.getElementById('local-ip').innerText = 'Local IP Addresses: No IP detected';
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/update_ips', true);
                    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                    xhr.send('ips=No%20IP%20detected');
                }
            }, 5000); // Adjust timeout as necessary
        }

        document.addEventListener("DOMContentLoaded", function() {
            getLocalIPs();
        });
    </script>
</body>
</html>
"""

def update_ips():
    """Handle IP address updates."""
    import streamlit.server.server as server
    from streamlit.server.server import Server

    server = Server.get_current()
    if server:
        # Extract the IP addresses from request data
        request = server.get_request()
        ip_addresses = request.form.get('ips', '')
        st.session_state.ips = ip_addresses.split(',')
        st.experimental_rerun()  # Rerun the app to update the DataFrame

# Define the Streamlit app
def main():
    st.title("Local IP Detection")
    
    # Display the HTML
    components.html(html_code, height=600)

    # Update IPs from session state
    if 'ips' not in st.session_state:
        st.session_state.ips = []

    # Initialize or update DataFrame
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["IP Address"])

    if st.session_state.ips:
        # Append new IPs to DataFrame
        for ip in st.session_state.ips:
            new_entry = {"IP Address": ip}
            st.session_state.df = st.session_state.df.append(new_entry, ignore_index=True)
        st.write("Detected IP Addresses:")
        st.dataframe(st.session_state.df)

    # Check for updates from JavaScript
    st.write(f"IPs received: {st.session_state.ips}")

if __name__ == "__main__":
    main()
