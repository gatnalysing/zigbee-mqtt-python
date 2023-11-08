import sys
import time
import subprocess

def power_cycle(relays):
    cycles = [
        (5, 5),    # (off time, on time)
        (5, 5),
        (5, 5),
        (5, 10),   # Flashing 10 seconds
        (5, 5),
        (5, None), # Leave on after this cycle
    ]
    
    for off_time, on_time in cycles:
        # Turn specified relays OFF
        for relay in relays:
            subprocess.run(["python", "opta.py", "OFF", str(relay)])
            time.sleep(0.5)  # Delay between commands
        
        print("-", end="", flush=True)
        time.sleep(off_time)
        
        # Turn specified relays ON
        for relay in relays:
            subprocess.run(["python", "opta.py", "ON", str(relay)])
            time.sleep(0.5)  # Delay between commands
            
        print("+", end="", flush=True)
        
        if on_time is not None:
            if on_time == 10:
                print("F", end="", flush=True)  # Indicate flashing
            time.sleep(on_time)
        else:
            print("Done!", end="\n", flush=True)
            break

def parse_args(args):
    relays = set()
    for arg in args:
        if arg.lower() == 'a':
            relays.update({1, 2, 3, 4})
        else:
            relays.update({int(digit) for digit in arg if digit.isdigit() and 1 <= int(digit) <= 4})
    return list(relays)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        relays = parse_args(sys.argv[1:])
        if not relays:
            print("Invalid input. Please provide relay numbers (1-4) or 'a' for all relays.")
        else:
            power_cycle(relays)
    else:
        print("No arguments provided. Please run the script with relay numbers (1-4) or 'a' for all relays.")
