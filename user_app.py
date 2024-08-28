import streamlit as st
import streamlit.components.v1 as components

# HTML and JavaScript code
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
        function getLocalIPs(callback) {
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
                        console.log('Detected IP:', ip[0]);
                        document.getElementById('local-ip').innerText = 'Local IP Addresses: ' + ips.join(', ');
                        window.parent.postMessage({type: 'local_ip', ips: ips}, '*');
                    }
                }
            };

            setTimeout(() => {
                if (ips.length === 0) {
                    document.getElementById('local-ip').innerText = 'Local IP Addresses: No IP detected';
                    window.parent.postMessage({type: 'local_ip', ips: ['No IP detected']}, '*');
                }
            }, 5000); // Adjust timeout as necessary
        }

        document.addEventListener("DOMContentLoaded", function() {
            getLocalIPs(function(ips) {
                // Callback to update IPs
            });
        });

        window.addEventListener("message", function(event) {
            if (event.data.type === 'local_ip') {
                window.parent.postMessage({type: 'local_ip', ips: event.data.ips}, '*');
            }
        });
    </script>
</body>
</html>
"""

# Streamlit app
def main():
    st.title("Local IP Detection")
    components.html(html_code, height=600)

if __name__ == "__main__":
    main()
