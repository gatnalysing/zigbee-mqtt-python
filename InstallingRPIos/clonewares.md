Based on the space used on generic Raspberry Pi lite installation on SSD (2.6 GB on the root and 61 MB on the boot partition), it's a good idea to allocate a bit more space to ensure all data fits comfortably. Using 2.7 GB or even rounding up to 3 GB for the image file would be prudent. This provides some buffer space for filesystem overheads and potential changes before cloning.

1. Unmount partitions:
   ```
   sudo umount /media/user/bootfs
   ```
   ```
   sudo umount /media/user/rootfs
   ```

2. Allocate space for the image file (3 GB):
   ```
   fallocate -l 3G /home/user/vanilla/clone.img
   ```

3. Set up the loop device:
   ```
   sudo losetup -fP /home/user/vanilla/clone.img
   ```
   ```
   losetup -a | grep clone.img
   ```

4. Create and format partitions (assuming `loop0` is assigned):
   ```bash
   sudo fdisk /dev/loop0
   sudo mkfs.vfat /dev/loop0p1
   sudo mkfs.ext4 /dev/loop0p2
   ```

5. Mount the loop device partitions:
   ```
   sudo mount /dev/loop0p1 /mnt/target_boot
   sudo mount /dev/loop0p2 /mnt/target_root
   ```

6. Copy data with `rsync`:
   ```
   sudo rsync -axHAWX --numeric-ids /media/user/bootfs/ /mnt/target_boot/
   sudo rsync -axHAWX --numeric-ids /media/user/rootfs/ /mnt/target_root/
   ```

7. Unmount and detach the loop device:
   ```
   sudo umount /mnt/target_boot
   sudo umount /mnt/target_root
   sudo losetup -d /dev/loop0
   ```

This approach will create an efficient image of your Raspberry Pi's SSD, suitable for cloning onto other devices.

For my purposes, I will need to remember to make the following changes after cloning a node:

1. Run `sudo raspi-config` and:
   - expand partition to use entire drive
   - chanage the hostname from generic one
   
3. create my wireguard configuration file
   ```
   sudo nano /etc/wireguard/wg0.conf
   ```
4. run `npm start` for the first time
   - with ConBeeII USB plugged in
5. close it:
   `ctrl`+`C`
6. enable zigbee2mqtt as a service:
   ```
   sudo systemctl enable zigbee2mqtt
   ```
7. start the service:
   ```
   sudo systemctl start zigbee2mqtt
   ```
8. Check the status of the service:
   ```
   systemctl status zigbee2mqtt.service
   ```
