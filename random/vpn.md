Here's a step-by-step guide to set up WireGuard on your Raspberry Pi:

### 1. Update and Upgrade:

Before you start, ensure your Raspberry Pi's OS is up-to-date:

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install WireGuard:

Install WireGuard using:

```bash
sudo apt install -y wireguard
```

### 3. Generate Key Pair for the Raspberry Pi:

```bash
umask 077
wg genkey | sudo tee /etc/wireguard/privatekey | wg pubkey | sudo tee /etc/wireguard/publickey
```

### 4. Configure WireGuard:

Create a WireGuard configuration file:

```bash
sudo nano /etc/wireguard/wg0.conf
```

Add the following content:

```plaintext
[Interface]
Address = 10.0.0.1/24
PrivateKey = [Private Key]
ListenPort = 51820

# Replace [Private Key] with the actual private key you generated before

# You will add the peer (VM and other RPi gateways) info here later
```

In case you need to retrieve your private key again:
```bash
sudo cat /etc/wireguard/privatekey
```

### 5. Activate WireGuard on the Raspberry Pi:

```bash
sudo wg-quick up wg0
```

### 6. Make WireGuard Start on Boot:

To ensure that the WireGuard service starts automatically when the Raspberry Pi boots up, enable the `wg-quick@wg0` service:

```bash
sudo systemctl enable wg-quick@wg0
```

### 7. Configure Port Forwarding (if needed):

If your Raspberry Pi is behind a router and you want to access it from outside of your local network, you'll need to configure port forwarding on your router to forward UDP traffic on port `51820` to your Raspberry Pi.

---

At this point the Raspberry Pi is set up as a WireGuard server
