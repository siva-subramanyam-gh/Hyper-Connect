import subprocess
import re
import os

class ADBManager:
    def __init__(self):
        pass

    # --- CONNECTION METHODS ---
    def check_usb_connection(self):
        """Checks if a device is connected via USB."""
        try:
            # capture_output=True keeps the terminal clean
            res = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            if "device" in res.stdout and "List of devices attached" in res.stdout:
                # Simple check: is the output longer than just the header?(because device not necessarily checks in next line)
                lines = res.stdout.strip().split('\n')
                return len(lines) > 1
            return False
        except Exception as e:
            print(f"Error checking USB: {e}")
            return False

    def connect_wireless(self, ip_address):
        """Switches to TCP/IP and connects to the phone."""
        try:
            subprocess.run(["adb", "tcpip", "5555"], timeout=5)
            res = subprocess.run(["adb", "connect", ip_address], capture_output=True, text=True)
            return "connected" in res.stdout
        except Exception as e:
            print(f"Error Wireless: {e}")
            return False

    # --- ACTION METHODS ---
    def send_text(self, text):
        if not text:
            return False 
        # Replace spaces with %s for ADB
        clean_text = text.replace(" ", "%s").replace("'", "").replace('"', "")
        
        try:
            subprocess.run(["adb", "shell", "input", "text", clean_text])
            return True
        except Exception as e:
            print(f"Error sending text: {e}")
            return False
        
    def pull_latest_photo(self,target_folder="./"):
        try:
            camera_path="/storage/emulated/0/DCIM/Camera/"
            cmd=f"ls -t {camera_path}"
            res=subprocess.run(["adb","shell",cmd],capture_output=True,text=True)
            lines=res.stdout.strip().splitlines()
            if not lines:
                print("No photos found or error reading folder.")
                return False
            filename=lines[0].strip()
            print(f"Found latest photo:{filename}")
            clean_path=f"{camera_path}"
            remote_path=f"{camera_path}{filename}"
            local_full_path = os.path.join(target_folder, filename)
            subprocess.run(["adb","pull",remote_path,local_full_path])
            return filename
        except Exception as e:
            print(f"Error pulling File:{e}")
            return False


    # --- SENSOR METHODS ---
    def get_battery_status(self):
        """Returns tuple (level, temperature) or None."""
        try:
            res = subprocess.run(['adb', 'shell', 'dumpsys', 'battery'], capture_output=True, text=True)
            output = res.stdout
            l_match = re.search(r'level: (\d+)', output)
            t_match = re.search(r'temperature: (\d+)', output)
            
            if l_match and t_match:
                return int(l_match.group(1)), int(t_match.group(1))
            return None
        except Exception as e:
            print(f"Error getting battery: {e}")
            return None

    def set_power_mode(self, enable: bool):
        """Toggles Power Saver Mode via Global Settings."""
        val = "1" if enable else "0"
        subprocess.run(['adb', 'shell', 'settings', 'put', 'global', 'low_power', val])