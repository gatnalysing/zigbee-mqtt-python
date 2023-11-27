
### `ziggypop.py` Script
- **Purpose**: Automates management of lamps connected to Deconz gateways.
- **Functions**:
  1. **Get Lamp Details**: Retrieves information about lamps from each Deconz gateway.
  2. **Rename Lamps**: Offers the option to rename lamps following a specific format.
  3. **Record Details**: Updates and records details of lamps into a readable text file.

### `zgindex.csv` Configuration File
- **Purpose**: Stores configuration data for each Deconz gateway.
- **Columns**:
  1. **name**: Identifier for the gateway.
  2. **description**: Human-readable description of the gateway.
  3. **ds**: Identifier used in lamp naming.
  4. **ip**: IP address of the gateway.
  5. **api**: API key for gateway access.

### How They Work Together
1. The script reads the `zgindex.csv` file to get details of each gateway.
2. It then communicates with the gateways using the IP addresses and API keys.
3. The script can rename lamps and fetches their updated details.
4. Finally, it generates a summary file for each gateway.

1. **Example `zgindex.csv`**:
   ```
   name,description,ds,ip,api
   example_gateway,example_location,123,192.168.1.100,API_KEY_HERE
   ```
   Replace `example_gateway`, `example_location`, `123`, `192.168.1.100`, and `API_KEY_HERE` with actual values.

2. **Instructions**:
   - Create a `zgindex.csv` file in the same directory as `ziggypop.py`
   - Run `ziggypop.py`
