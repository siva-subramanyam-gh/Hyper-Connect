import subprocess
import sys
def type_on_phone(text):
    clean_text=text.replace(" ","%s")
    cmd=['adb','shell','input','text',clean_text]
    subprocess.run(cmd)
    print(f"Sent to phone:{text}")
if __name__=="__main__":
    print("Type something and press enter to send (Type exit to quit):")
    while True:
        a=input(">")
        if a.lower()=="exit":
            break
        type_on_phone(a)