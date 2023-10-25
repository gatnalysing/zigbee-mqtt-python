# NixOS Installation Guide

## Download the NixOS ISO Image

You can download the NixOS ISO image from the following link:

[NixOS ISO Download Link](https://nixos.org/download#nixos-iso)

## Instructions for Booting from USB

For detailed instructions on how to create a bootable USB and more, refer to the official NixOS documentation:

[NixOS Booting from USB Instructions](https://nixos.org/manual/nixos/stable/#sec-booting-from-usb)

## Creating a Bootable USB

1. First, ensure that the USB device is unmounted:

    ```bash
    sudo umount /dev/sda
    ```

2. Write the downloaded ISO image to the USB device:

    ```bash
    sudo dd if=/home/user/Downloads/nixos-minimal-23.05.4407.80c1aab72515-x86_64-linux.iso of=/dev/sda bs=4M conv=fsync
    ```

**Note**: Make sure to replace `/dev/sda` with the correct device path for your USB drive. You can check the available devices with the `lsblk` or `fdisk -l` commands.

---

## Safety Warning

Always double-check your device path before using the `dd` command to avoid overwriting any important data.

---

That's it! You now have a bootable USB ready with NixOS.

