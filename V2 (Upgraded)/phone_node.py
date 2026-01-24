import socket 
import time
import sys

broadcast_port=5001
secret_key="HyperConnect_secure_token"

def find_server():
    '''Listen to UDP Broadcast to find the laptop's IP'''
    listener=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    listener.bind(('',broadcast_port))

    print("--Scanning for Hyperconnect Node--")
    data,addr=listener.recvfrom(1024)
    message=data.decode()
    if message.startswith("HYPER_DISCOVER"):
        server_ip=addr[0]
        server_port=int(message.split(":")[1])
        print(f"Found Noode at {server_ip}:{server_port}")
        return server_ip,server_port
    return None,None

def send_data(ip,port,text):
    '''Connects , then sends data and breaks the connection (Ephemeral)'''
    try:
        client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.settimeout(2)
        client.connect((ip,port))
        packet=f"{secret_key}::{text}"
        client.send(packet.encode('utf-8'))
        client.close()
        print("Data Sent Successfully.")
    except Exception as e:
        print(f"Send Failed :{e}")

if __name__=="__main__":
    target_ip,target_port=find_server()
    if target_ip:
        print("Type text to send (CTRL+C to quit):")
        while True:
            text=input(">> ")
            send_data(target_ip,target_port,text)
    