import customtkinter as ctk
import subprocess
import threading
import re
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")
class HyperConnectApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("HyperConnect-Bridge")
        self.geometry("800x600")

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

        #Label to show battery status
        self.battery_label=ctk.CTkLabel(self,text="Battery Status: N/A")
        self.battery_label.pack(pady=10)

        #Label to go Wireless Section
        self.wireless_label=ctk.CTkLabel(self,text="---Wireless Mode---",text_color="cyan")
        self.wireless_label.pack(pady=5)

        #Input for IPv4 address
        self.ip_text=ctk.CTkEntry(self,placeholder_text="Enter phone's IPv4 address here....")
        self.ip_text.pack(pady=5)

        #button to connect wirelessly
        self.btn_wireless=ctk.CTkButton(self,text="Connect Wirelessly",command=self.thread_wireless_connect)
        self.btn_wireless.pack(pady=10)

    def thread_check_adb(self):
        threading.Thread(target=self.check_adb).start()

    def thread_send_text(self):
        threading.Thread(target=self.send_text).start()

    def thread_check_battery(self):
        threading.Thread(target=self.check_battery).start()
    
    def thread_wireless_connect(self):
        threading.Thread(target=self.wireless_connect).start()

    def check_adb(self):
        try:
            res=subprocess.run(["adb","devices"],capture_output=True,text=True)
            if "device" in res.stdout and "List" in res.stdout:
                self.status_label.configure(text="Status: Connected",text_color="green")
            else:
                self.status_label.configure(text="Status: No device found",text_color="Orange")
        except Exception as e:
            self.status_label.configure(text=f"Status: Error {e} ",text_color="red")

    def send_text(self):
        text=self.text_entry.get()
        clean=text.replace(" ","%s")
        subprocess.run(["adb","shell","input","text",clean])
        print(f"Sent:{text}")

    def check_battery(self):
        try:
            result=subprocess.run(["adb","shell","dumpsys","battery"],capture_output=True,text=True)
            output=result.stdout
            level_match=re.search(r'level: (\d+)',output)
            level=level_match.group(1) if level_match else "Unknown"
            volt_match=re.search(r'voltage: (\d+)',output)
            voltage="Unknown"
            if volt_match:
                voltage=f"{int(volt_match.group(1))/1000:.2f}V"
            info = f"🔋 Battery: {level}% | ⚡ {voltage}"
            self.battery_label.configure(text=info,text_color="cyan")
        except Exception as e:
            print(f"Error {e}")

    def wireless_connect(self):
        ip=self.ip_text.get()
        if not ip:
            self.status_label.configure(text="Enter valid IP address first!",text_color="red")
            return
        self.status_label.configure(text="Switching to TCP/IP....",text_color="orange")
        subprocess.run(["adb","tcpip","5555"])
        result=subprocess.run(["adb","connect",ip],capture_output=True,text=True)
        if "connected to" in result.stdout:
            self.status_label.configure(text="Connected Wirelessly!",text_color="green")
            print(f"Success:{result.stdout}")
        else:
            self.status_label.configure(text="Connection Failed",text_color="red")
            print(f"Failed:{result.stdout}")

if __name__=="__main__":
    app=HyperConnectApp()
    app.mainloop()