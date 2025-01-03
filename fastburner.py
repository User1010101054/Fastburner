import os
import subprocess
import sys

def list_devices():
    print("Detecting available USB devices...")
    subprocess.run(["lsblk", "-o", "NAME,SIZE,TYPE,MOUNTPOINT"])

def burn_iso(iso_path, usb_device):
    print(f"Preparing to write {iso_path} to {usb_device}")
    
    if not os.path.isfile(iso_path):
        print("Error: ISO file not found!")
        return
    
    confirm = input(f"Are you sure you want to write to {usb_device}? This will erase all data (y/N): ").lower()
    if confirm != 'y':
        print("Operation canceled.")
        return
    
    print("Unmounting USB device...")
    subprocess.run(["umount", f"/dev/{usb_device}"], stderr=subprocess.DEVNULL)
    
    print("Starting burning process...")
    try:
        subprocess.run(["sudo", "dd", f"if={iso_path}", f"of=/dev/{usb_device}", "bs=4M", "status=progress"], check=True)
        subprocess.run(["sync"])  # Ensure data is fully written to the USB.
        print("Burning process completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("Failed to write the ISO. Please check the device and try again.")

def main():
    print("Welcome to FastBurner!")
    while True:
        print("\nOptions:")
        print("1. List available USB devices")
        print("2. Burn ISO to USB")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            list_devices()
        elif choice == '2':
            iso_path = input("Enter the path to the ISO file: ").strip()
            usb_device = input("Enter the USB device name (e.g., sdb): ").strip()
            burn_iso(iso_path, usb_device)
        elif choice == '3':
            print("Exiting FastBurner. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
