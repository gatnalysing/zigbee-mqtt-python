sudo fdisk -l

Device         Boot   Start      End  Sectors  Size Id Type
/dev/mmcblk0p1         8192  1056767  1048576  512M  c W95 FAT32 (LBA)
/dev/mmcblk0p2      1056768 31116287 30059520 14,3G 83 Linux

1. **Unmount SD Card Partitions**:
   ```bash
   sudo umount /dev/mmcblk0p1
   sudo umount /dev/mmcblk0p2
   ```

2. **Backup SD Card**:
   ```bash
   sudo dd if=/dev/mmcblk0 of=~/sdcard_backup.img bs=4M status=progress
   ```

3. **Safely Remove SD Card**:
   ```bash
   sync
   ```

sd-card backup (`sdcard_backup.img`) is saved in home directory.
