import pyperclip
import subprocess
import time
def send_to_phone(text):
    clean_text=text.replace(" ","%s").replace("'","").replace('"',"")
    cmd=["adb","shell","input","text",clean_text]
    subprocess.run(cmd)
    print(f"Sent new text to phone:{text}")
def main():
    print("---Clipboard Sync(Running)---")
    print("Enter text to send to your phone:")
    last_text=""
    while True:
        try:
            curr_text=pyperclip.paste()
            if curr_text!=last_text:
                send_to_phone(curr_text)
                last_text=curr_text
            time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping Sync.....")
            break
if __name__=="__main__":
    main()