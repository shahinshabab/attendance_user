import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

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

                        // Use a hidden form to send data to Streamlit
                        var form = document.createElement('form');
                        form.method = 'POST';
                        form.action = '/';
                        var input = document.createElement('input');
                        input.type = 'hidden';
                        input.name = 'ips';
                        input.value = ips.join(',');
                        form.appendChild(input);
                        document.body.appendChild(form);
                        form.submit();
                    }
                }
            };

            setTimeout(() => {
                if (ips.length === 0) {
                    document.getElementById('local-ip').innerText = 'Local IP Addresses: No IP detected';
                    var form = document.createElement('form');
                    form.method = 'POST';
                    form.action = '/';
                    var input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'ips';
                    input.value = 'No IP detected';
                    form.appendChild(input);
                    document.body.appendChild(form);
                    form.submit();
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

def main():
    st.title("Local IP Detection")
    
    # Display the HTML content
    components.html(html_code, height=600)
    
    # Initialize or update DataFrame
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["IP Address"])

    # Process form data
    if st.experimental_get_query_params().get('ips'):
        ips = st.experimental_get_query_params().get('ips', [''])[0]
        
        # Add new IPs to the DataFrame
        for ip in ips.split(','):
            new_entry = {"IP Address": ip}
            st.session_state.df = st.session_state.df.append(new_entry, ignore_index=True)

    # Display DataFrame
    st.write("Detected IP Addresses:")
    st.dataframe(st.session_state.df)

if __name__ == "__main__":
    main()
