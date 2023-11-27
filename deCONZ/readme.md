### `zgindex.csv` Configuration File (User Generated File)
- **Purpose**: Stores configuration data for each Deconz gateway.

`zgindex.csv`:
```
name,description,ds,ip,api
zg1,office_area,123,192.168.1.101,APIKEY1234
zg2,conference_room,456,192.168.1.102,APIKEY5678
zg3,lobby,789,192.168.1.103,APIKEY9012
```
Or in more human readible format:
| name   | description      | ds  | ip           | api        |
|--------|------------------|-----|--------------|------------|
| zg1    | office_area      | 123 | 192.168.1.101| APIKEY1234 |
| zg2    | conference_room  | 456 | 192.168.1.102| APIKEY5678 |
| zg3    | lobby            | 789 | 192.168.1.103| APIKEY9012 |

### `ziggystates.py` Script
1. The script reads the `zgindex.csv` file to get details of each gateway.
2. It then communicates with the gateways using the IP addresses and API keys.
3. The script can rename lamps and fetches their updated details.
4. Finally, it generates a summary file for each gateway including a list of devices:

```
zg06.txt
name: zg01
description: office_area
ds: 483
ip: 192.168.1.101
api: APIKEY1234
api total: 5
count: 5
devices: (
	123-lampi001
	123-lampi002
	123-lampi003
	123-lampi004
	123-lampi005
  )
```

### `ziggystates.py` Script
- **Function**: Fetches and records the states of lamps from Deconz gateways.
- **Process**:
  1. **Reads**: `zgindex.csv` for gateway details.
  2. **Fetches**: Lamp states via API calls.
  3. **Writes**: Outputs to files named `zgXstate.txt` (X represents the gateway name).

### Example Output (`zg01state.txt`)
- Contains gateway details and state of each lamp (ID, Name, Type, State).
  
```
name: zg1
description: office_area
ds: 123
ip: 192.168.1.101
api: APIKEY1234
Lamps:
  Lamp ID: 1
    Name: 123-lampi001
    Type: Extended color light
    State: {'alert': 'none', 'bri': 254, 'colormode': 'xy', 'ct': 186, 'effect': 'none', 'hue': 54612, 'on': True, 'reachable': False, 'sat': 254, 'xy': [0.1355, 0.0399]}

  Lamp ID: 2
    Name: 123-lampi002
    Type: Dimmable light
    State: {'alert': 'none', 'bri': 254, 'on': True, 'reachable': False}

  Lamp ID: 3
    Name: 123-lampi003
    Type: Extended color light
    State: {'alert': 'none', 'bri': 254, 'colormode': 'xy', 'ct': 186, 'effect': 'none', 'hue': 54612, 'on': True, 'reachable': True, 'sat': 254, 'xy': [0.2725, 0.1096]}

  Lamp ID: 4
    Name: 123-lampi004
    Type: Dimmable light
    State: {'alert': 'none', 'bri': 254, 'on': True, 'reachable': True}

  Lamp ID: 5
    Name: 123-lampi005
    Type: Extended color light
    State: {'alert': 'none', 'bri': 254, 'colormode': 'xy', 'ct': 249, 'effect': 'none', 'hue': 54612, 'on': True, 'reachable': True, 'sat': 120, 'xy': [0.7006, 0.2993]}

```

**Initial setup instructions**:
   - Create a `zgindex.csv` file like the one above
   - Generate the colour index file `colours.txt` of the colours intended to be used
   - Run:
     - `ziggypop.py`    creates --> device zg lists `zgXXX.txt`
     - `ziggystates.py` creates --> status zg lists `zg06state.txt`
   - python API scripts are now ready to be run
     - `deCONZserialRGB.py` attempts to change colour of all RGB capable lamps on gateway, one-by-one.
     - Usage/example:
       ```
       python3 deCONZserialRGB.py [identifier] [colour] [brightn.] [fade(sec.)] [iteration(sec.)]
       ```
       ```
       python3 deCONZserialRGB.py zg1 RED 210 10 2
       ```

     - `deCONZserialRGB.py` changes the colour of a single lamp on a gateway.
     - Usage/example:
       
       ```
       python3 deCONZcolour.py [identifier] [lamp_nr] [colour] [brightn.] [fade(sec.)]
       ```
       ```
       python3 deCONZcolour.py zg1 1 RED 210 2
       ```
