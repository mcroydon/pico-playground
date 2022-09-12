import network, socket, time

ssid = 'MY_SSID'
password = 'MY_PASSWORD'

# Set up WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Connect to WLAN
max_wait = 5
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    time.sleep(1)

# Don't proceed if there's an error
if wlan.status() != 3:
    raise RuntimeError("Network connection failure.")

# Connect to time.nist.gov using the TIME protocol on TCP Port 37
s = socket.socket()
s.connect(socket.getaddrinfo("time.nist.gov", 37)[0][-1])

# Recieve a 32 bit integer result (in bytes).
result = s.recv(32)

# Convert from bytes to integer (Big Endian)
int_result = int.from_bytes(result, "big")

# TIME protocol epoch is Jan 1 1900. Convert to Jan 1 1970.
epoch_result = int_result - 2208988800

# Print time if we recieved a valid response from the server.
if int_result > 0:
    print(f"Seconds since 1900: {int_result}")
    print(f"Seconds since 1970: {epoch_result}")
    tt = time.gmtime(epoch_result)
    print(f"The time is {tt[0]}-{tt[1]:02}-{tt[2]:02} {tt[3]:02}:{tt[4]:02}:{tt[5]:02}Z")
else:
    print("Bad response from server.")