import customtkinter as ctk
import subprocess
import threading
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

    def thread_check_adb(self):
        threading.Thread(target=self.check_adb).start()

    def thread_send_text(self):
        threading.Thread(target=self.send_text).start()

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

if __name__=="__main__":
    app=HyperConnectApp()
    app.mainloop()