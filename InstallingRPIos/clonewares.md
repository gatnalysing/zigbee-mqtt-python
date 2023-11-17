sudo umount /media/user/bootfs
sudo umount /media/user/rootfs

fallocate -l 3G /home/user/clondir/clone.img

sudo losetup -fP /home/user/clondir/clone.img

losetup -a | grep clone.img

sudo fdisk /dev/loop0

sudo mkfs.vfat /dev/loop0p1
sudo mkfs.ext4 /dev/loop0p2

sudo mount /dev/loop0p1 /mnt/target_boot
sudo mount /dev/loop0p2 /mnt/target_root

sudo rsync -axHAWX --numeric-ids /media/user/bootfs/ /mnt/target_boot/
sudo rsync -axHAWX --numeric-ids /media/user/rootfs/ /mnt/target_root/

sudo umount /mnt/target_boot
sudo umount /mnt/target_root

sudo losetup -d /dev/loop0
