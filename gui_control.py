import customtkinter as ctk
import subprocess
import threading
import re
from backend import ADBManager

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")
class HyperConnectApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("HyperConnect-Bridge")
        self.geometry("800x600")
        self.adb=ADBManager()
        #Label status of connection
        self.status_label=ctk.CTkLabel(self,text="Status: Disconnected",text_color="red")
        self.status_label.pack(pady=20)

        #Button to Initialize the connection
        self.btn_connect=ctk.CTkButton(self,text="Initialize Connection",command=self.thread_check_adb)
        self.btn_connect.pack(pady=10)

        #Button to ghost type on phone
        self.text_entry=ctk.CTkEntry(self,placeholder_text="Type Text here....")
        self.text_entry.pack(pady=10)

        #Button to send the text to phone
        self.btn_send=ctk.CTkButton(self,text="Send to phone",command=self.thread_send_text)
        self.btn_send.pack(pady=10)

        #Button to check battery status
        self.btn_check_battery=ctk.CTkButton(self,text="Check Battery Status",command=self.thread_check_battery)
        self.btn_check_battery.pack(pady=10)

        #Label to go Wireless Section
        self.wireless_label=ctk.CTkLabel(self,text="---Wireless Mode---",text_color="cyan")
        self.wireless_label.pack(pady=5)

        #Input for IPv4 address
        self.ip_text=ctk.CTkEntry(self,placeholder_text="Enter phone's IPv4 address here....")
        self.ip_text.pack(pady=5)

        #button to connect wirelessly
        self.btn_wireless=ctk.CTkButton(self,text="Connect Wirelessly",command=self.thread_wireless_connect)
        self.btn_wireless.pack(pady=10)

        #Button to backup latest photo
        self.btn_photo = ctk.CTkButton(self, text="Backup Latest Photo", command=self.run_photo_backup)
        self.btn_photo.pack(pady=5)

#----Threading Methods to prevent UI from freezing with Actions----
    def thread_check_adb(self):
        threading.Thread(target=self._usb_logic).start()

    def thread_send_text(self):
        threading.Thread(target=self.text_logic).start()

    def thread_check_battery(self):
        threading.Thread(target=self.battery_logic).start()
    
    def thread_wireless_connect(self):
        threading.Thread(target=self.wireless_logic).start()

    def run_photo_backup(self):
        threading.Thread(target=self.photo_logic).start()

#----Actual calling methods to adbcore
    def _usb_logic(self):
        success=self.adb.check_usb_connection()
        if success:
            self.status_label.configure(text="Status: Device Connected",text_color="green")
        else:
            self.status_label.configure(text="Status: No Device Found",text_color="red")
    
    def text_logic(self):
        text=self.text_entry.get()
        success=self.adb.send_text(text)
        if success:
            self.status_label.configure(text="Status: Text Sent Successfully",text_color="green")
        else:
            self.status_label.configure(text="Status: Failed to send Text",text_color="red")

    def battery_logic(self):
        data = self.adb.get_battery_status()
        if data:
            level, temp = data # Unpack the tuple
            info = f"🔋 Battery: {level}% | 🌡️ Temp: {temp/10:.1f}°C"
            self.status_label.configure(text=info, text_color="cyan")
        else:
            self.status_label.configure(text="Error: Could not read battery", text_color="orange")

    def wireless_logic(self):
        ip = self.ip_text.get()
        if not ip:
            self.status_label.configure(text="Error: Enter IP first", text_color="orange")
            return
        self.status_label.configure(text="Status: Switching to TCP/IP...", text_color="yellow")
        success = self.adb.connect_wireless(ip)
        
        if success:
            self.status_label.configure(text=f"Connected to {ip}", text_color="green")
        else:
            self.status_label.configure(text="Wireless Connection Failed", text_color="red")

    def photo_logic(self):
        self.status_label.configure(text="Status: Pulling Photo",text_color="orange")
        name=self.adb.pull_latest_photo()
        if name:
            self.status_label.configure(text=f"Status: Saved {name}",text_color="green")
        else:
            self.status_label.configure(text="Error: Pull Failed", text_color="red")



if __name__=="__main__":
    app=HyperConnectApp()
    app.mainloop()