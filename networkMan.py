import network
import time
import sys
import select







# Network credentials
HOSTNAME = "mbesp32"
HOME_SSID = "BELL904"





def set_hostname(wlan):
    """Set the same hostname for all network types."""
    try:
        wlan.config(dhcp_hostname=HOSTNAME)  # Set hostname
        print(f"Hostname set to: {HOSTNAME}")
    except Exception as e:
        print(f"Failed to set hostname: {e}")

def connect_to_wifi(ssid, password=None):
    """Try connecting to a network with appropriate settings."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    set_hostname(wlan)  # Set the hostname

    try:
        print(f"Connecting to {ssid}.")
        wlan.connect(ssid, password)

        # Wait for connection
        start = time.time()
        while not wlan.isconnected():
            if time.time() - start > 10:  # Timeout after 20 seconds
                raise TimeoutError(f"Connection to {ssid} timed out.")
            time.sleep(1)

        print(f"Connected to {ssid}!")
        print("IP Address:", wlan.ifconfig()[0])
        return True  # Success

    except Exception as e:
        print(f"Error connecting to {ssid}: {e}")
        return False  # Failure

def setup_access_point():
    """Set up the ESP32 as an access point if all networks fail."""
    print("Setting up Access Point...")
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    # ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.10.1', '8.8.8.8'))
    ap.config(essid='ESP32-AccessPoint', password='123456789', authmode=network.AUTH_WPA_WPA2_PSK)
    set_hostname(ap)  # Set the same hostname for AP
    print("Access Point is active. IP:", ap.ifconfig()[0]) # i believe it defaults to 192.168.4.1 everytime
    # so access using http:\\192.168.4.1 or maybe "ESP32 Web Server" in the broswer might work

def scan_networks():
    """Scan for available Wi-Fi networks."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()  # List of tuples (ssid, bssid, channel, RSSI, authmode, hidden)
    return [net[0].decode('utf-8') for net in networks]

def timed_selection(options, prompt="Select an option: ", timeout=10):
    """Allow the user to select an option with a timeout."""
    print(prompt)
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")

    start = time.time()
    result = ''

    while time.time() - start < timeout:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            char = sys.stdin.read(1)
            if char in ['\n', '\r']:  # Enter key pressed
                break
            result += char

    if result.isdigit() and 1 <= int(result) <= len(options):
        return options[int(result) - 1]

    print("Selection timed out or invalid input.")
    return None


def timed_input(prompt, timeout=10):
    """Input function with a timeout."""
    print(prompt)
    result = ''
    start = time.time()

    while time.time() - start < timeout:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            char = sys.stdin.read(1)
            if char in ['\n', '\r']:  # Enter key pressed
                break
            result += char
            print('*', end="")  # Mask input with '*'

    print()  # Move to the next line
    if not result:
        print("Input timed out.")
    return result


def run_connect():
    """Main function to handle the connection logic."""
    #print("Starting network connection sequence...")
    # "EFDA9EAE2D15"
    
    print("Scanning for available networks...")
    networks = scan_networks()

    if not networks:
        print("No networks found. Setting up Access Point...")
        setup_access_point()
        return
    
    ssid = timed_selection(networks, prompt="Select a network to connect to:", timeout=10)

    if not ssid:
        print("No network selected. Setting up Access Point...")
        setup_access_point()
        return

    # Get the password with a timeout
    # print(home_password)

    
    if(ssid == "FanshaweCollege"):
        username = timed_input(f"Enter username for {ssid} (10s): ", timeout=10)
        password = timed_input(f"Enter password for {ssid} (10s): ", timeout=10)
        
        if connect_to_college_wifi(ssid, username, password):
            return 
        else:
            return setup_access_point()
    else:
        password = timed_input(f"Enter password for {ssid} (10s): ", timeout=10)
    



    if not password:
        print("No password entered. Setting up Access Point...")
        setup_aSccess_point()
        return


    if connect_to_wifi(ssid, password=password):
        return


    # default to connect to laptop network then phone then access point
    print("Failed to connect to the selected network.")
    setup_access_point()






















def connect_to_college_wifi(ssid, username, password):
    """Attempt to connect to the WPA2-Enterprise network."""
    #anonymous_identity = "anon"
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    set_hostname(wlan)

    try:
        wlan.config(
            #eap='TTLS',
            username=username,
            #anonymous_identity="anon",
            password=password,
            # phase2='PAP'
        )

        print(f"Connecting to {ssid}...")
        wlan.connect(ssid)

        start = time.time()
        while not wlan.isconnected():
            if time.time() - start > 20:
                raise TimeoutError("Connection timed out.")
            time.sleep(1)

        print(f"Connected to {ssid}!")
        print("IP Address:", wlan.ifconfig()[0])
        return True

    except Exception as e:
        print(f"Error connecting to {ssid}: {e}")
        return False