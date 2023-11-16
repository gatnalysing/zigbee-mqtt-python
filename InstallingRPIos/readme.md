Peripherals:
1. Connect ConBee2 & SSD to USB 2.0 ports. It's important not to use 3.0 as it causes issues
2. HDMI, ethernet, mouse, keyboard
3. plug in USB-C to power on

4. Network installation:
   - hold 'shift' and wait for network installation to initiate
   - select 'is' for keyboard layout and english for language

5. Configurations:
   - hostname
   - enable SSH
   - username
   - password
   - set locale (keyb:is lang:eng)
   - uncheck "Eject"
   - 'Write' (installs and reboots)

6. First bootup:
   - login using username and password set during install configuration
   - take note of IP address
     ```
     ip a
     ```
   - update and upgrade
     ```
     sudo apt update
     ```
     ```
     sudo apt upgrade
     ```
  7. Configure Raspberry Pi
     ```
     sudo raspi-config
     ```
     - (5) Localisation Options
       - (L1) Locale:
         - make sure enGB & is_IS are selected
         - select en_GB as default
     - (6) Advanced Options
       - (A1) Expand Filesystem
       - (A5) Update Bootloader
     - 'Esc' -> 'Finish' & reboot
  8. System configuration complete
     ```
     sudo shutdown now
     ```
  9. Software Installation:
      - "ssh"
      - 
