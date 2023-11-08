__all__ = ["publish_message"]

import serial
import sys
import time

def send_serial_command(command):
    ser = serial.Serial('/dev/ttyACM0', 11520, timeout=1)
    ser.flush()

    try:
        ser.write((command + '\n').encode('utf-8'))
        print(f"Command `{command}` sent to Arduino")
    except Exception as e:
        print(f"Failed to send command to Arduino: {str(e)}")
    finally:
        ser.close()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        action = sys.argv[1].upper()
        relay_num = sys.argv[2].upper()

        if action in ["ON", "OFF"] and (relay_num.isdigit() or relay_num == 'A'):
            if relay_num == 'A':
                for i in range(1, 5):
                    command = f"{i}" if action == "ON" else f"{i+4}"
                    send_serial_command(command)
                    time.sleep(0.1)  # Wait a little bit before sending the next command
            else:
                relay_num = int(relay_num)
                command = f"{relay_num}" if action == "ON" else f"{relay_num+4}"
                send_serial_command(command)
        else:
            print("Invalid arguments. Please use ON/OFF and a relay number or 'A' for all.")
    else:
        print("Not enough arguments provided. Please run the script with ON/OFF and a relay number or 'A>
