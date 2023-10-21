
**WireGuard VPN Configuration Generator**
*(for people with ADHD)*

These instructions contain a Python script to set up a WireGuard VPN server on Ubuntu and generate configurations for up to 30 clients. 

<br/>
The script also creates a CSV file with client details for easy reference.

#### Prerequisites

- Ubuntu system with WireGuard installed.
- Python 3.x

#### Instructions

1. **Create the python script:** (select/create directory and nano "wireguard_config_gen.py")

   ```python
	import os
	import subprocess

	CLIENT_COUNT = 30
	BASE_IP = "10.0.0."
	START_IP_NUM = 2  # starting from 10.0.0.2 for the first client
	CSV_FILENAME = "client_data.csv"

	# Check if wireguard tools are available
	if not os.path.exists("/usr/bin/wg"):
	    print("WireGuard tools are not found. Please install WireGuard.")
	    exit(1)

	def generate_key_pair():
	    private_key = subprocess.getoutput("wg genkey")
	    public_key = subprocess.getoutput(f"echo {private_key} | wg pubkey")
	    return private_key, public_key

	# Generate server keys
	server_private, server_public = generate_key_pair()

	# Server config setup
	server_config = f"""[Interface]
	Address = {BASE_IP}1/24
	ListenPort = 51820
	PrivateKey = {server_private}
	PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
	PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
	"""

	with open("/etc/wireguard/wg0.conf", "w") as f:
	    f.write(server_config)

	# CSV header
	csv_data = "Client Name,Private Key,Public Key,Assigned IP\n"

	for i in range(1, CLIENT_COUNT + 1):
	    client_private, client_public = generate_key_pair()
	    client_name = f"client{i}"
	    client_ip = BASE_IP + str(START_IP_NUM + i - 1)
	    
	    # Update server config with client data
	    server_config += f"""
	[Peer]
	PublicKey = {client_public}
	AllowedIPs = {client_ip}/32
	"""

	    # Create client config
	    client_config = f"""[Interface]
	Address = {client_ip}/24
	PrivateKey = {client_private}

	[Peer]
	PublicKey = {server_public}
	Endpoint = <YourExternalIPAddress>:51820
	AllowedIPs = 0.0.0.0/0
	"""
	    with open(f"{client_name}.conf", "w") as f:
		f.write(client_config)

	    # Update CSV data
	    csv_data += f"{client_name},{client_private},{client_public},{client_ip}\n"

	# Save updated server config
	with open("/etc/wireguard/wg0.conf", "w") as f:
	    f.write(server_config)

	# Save CSV data
	with open(CSV_FILENAME, "w") as f:
	    f.write(csv_data)

	print(f"Configuration files generated. CSV data saved to {CSV_FILENAME}.")

   ```

   **eth0 Important note:** The code block above makes a lot of assumptions. For example eth0 might not be your uplink device
<br/>
2. **Script Setup**  
   Save the provided Python script in the repository as `wireguard_config_gen.py`.
<br/>
3. **Make the Script Executable**

   ```bash
   sudo chmod +x wireguard_config_gen.py
   ```

4. **Execute the Script**  
   Run the script with root privileges to generate the server and client configuration files, as well as the CSV file.

   ```bash
   sudo python3 wireguard_config_gen.py
   ```
<br/>
After execution, you should have:

- A server configuration file at `/etc/wireguard/wg0.conf`.
- A configuration file for each client named `clientX.conf` in the current directory (where `X` is the client number from 1 to 30).
- A CSV file named `client_data.csv` with details about each client.

*The CSV is just intended as a way to easily manage vpn nodes*
