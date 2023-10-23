import time
import plc  # Import the plc module

def power_cycle():
    cycles = [
        (5, 5),  # (off time, on time)
        (5, 5),
        (5, 5),
        (5, 10),  # Flashing 10 seconds
        (5, 5),
        (5, None),  # Leave on after this cycle
    ]
    
    total_steps = len(cycles) * 2
    current_step = 0
    
    for i, (off_time, on_time) in enumerate(cycles, start=1):
        current_step += 1
        plc.publish_message("OFF")
        print(f"Step {current_step}/{total_steps}: Power OFF - Cycle {i}")
        time.sleep(off_time)
        
        current_step += 1
        plc.publish_message("ON")
        print(f"Step {current_step}/{total_steps}: Power ON - Cycle {i}")
        
        if on_time is not None:
            if on_time == 10:
                print("Flashing Lights!")
            time.sleep(on_time)
        else:
            print("Leaving lights ON")
            print("Sequence complete!")
            break

if __name__ == "__main__":
    power_cycle()
