
### WireGuard VPN Configuration Generator

This repository contains a Python script to set up a WireGuard VPN server on Ubuntu and generate configurations for up to 30 clients. The script also creates a CSV file with client details for easy reference.

#### Prerequisites

- Ubuntu system with WireGuard installed.
- Python 3.x

#### Instructions

1. **Clone the Repository** (Assuming you will place the Python script in this repo)

   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Script Setup**  
   Save the provided Python script in the repository as `wireguard_config_gen.py`.

3. **Make the Script Executable**

   ```bash
   sudo chmod +x wireguard_config_gen.py
   ```

4. **Execute the Script**  
   Run the script with root privileges to generate the server and client configuration files, as well as the CSV file.

   ```bash
   sudo python3 wireguard_config_gen.py
   ```

After execution, you should have:

- A server configuration file at `/etc/wireguard/wg0.conf`.
- A configuration file for each client named `clientX.conf` in the current directory (where `X` is the client number from 1 to 30).
- A CSV file named `client_data.csv` with details about each client.

Upload the CSV to Google Sheets or another spreadsheet application for easy reference and management.

#### Note

For security reasons, DO NOT upload private keys or configuration files containing private keys to public repositories or public locations.

---
.md Created with the help of GPT
