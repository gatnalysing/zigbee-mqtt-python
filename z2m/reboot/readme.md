To run your `reboot.py` script as a service, you can create a systemd service file. This allows the script to start automatically at boot up. 
Step-by-step guide:

1. **Create a Service File**: First, create a systemd service file for your script.

   Create a new service file 
   
   ```bash
   sudo nano /etc/systemd/system/reboot_script.service
   ```

   Add the following:

   ```ini
   [Unit]
   Description=Python Reboot Script Service
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /home/user/pythontools/reboot/reboot.py
   WorkingDirectory=/home/user/pythontools/reboot/
   StandardOutput=inherit
   StandardError=inherit
   Restart=always
   User=user

   [Install]
   WantedBy=multi-user.target
   ```

   Replace `/path/to/your/reboot.py` and `/path/to/your/` with the path to your `reboot.py` script.
   Replace `user` with your user name

3. **Enable and Start the Service**: Once you've created the service file, you need to start and enable it so that it runs on boot.

   Reload the systemd manager configuration:
   
   ```bash
   sudo systemctl daemon-reload
   ```

   Start the service:
   
   ```bash
   sudo systemctl start reboot_script.service
   ```

   Enable the service to run on boot:
   
   ```bash
   sudo systemctl enable reboot_script.service
   ```
