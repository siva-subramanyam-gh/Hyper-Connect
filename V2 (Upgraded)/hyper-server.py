import socket 
import threading
import time
import pyperclip
import ssl

#Defining ports for Broadcast and Data transfer
Broadcast_port=5001
Data_port=6000
Secret_key="HyperConnect_secure_token"  # Simple token for security handshake

def broadcast_presence():
    '''Sending a UDP beacon for our phone / other devices to identify our presence '''
    udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    print(f"---Broadcast Beacon Active via Port : {Broadcast_port}")
    while True:
        message=f"Hyper Discover:{Data_port}"
        try:
            udp.sendto(message.encode(), ('172.22.7.36', Broadcast_port))
            time.sleep(2)
        except Exception as e:
            print(f"Beacon error:{e}")
            time.sleep(5)
def handle_client(conn):
    """Handles the secure data transfer"""
    try:
        data=conn.recv(4096).decode('utf-8')
        if data.startswith(Secret_key):
            payload=data.split("::")[1]
            print(f"Synced {payload}")
            pyperclip.copy(payload)
        else:
            print("Security error:Invalid Token Recieved")
    except Exception as e:
        print(f"Transfer error :{e}")
    finally:
        conn.close()

def start_data_listener():
    tcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp.bind(('0.0.0.0',Data_port))
    tcp.listen()
    print(f"Data Listener Active on Port {Data_port}")
    try:
        while True:
            conn, addr = tcp.accept()
            threading.Thread(target=handle_client, args=(conn,)).start()
    except Exception as e:
        print(e)

if __name__=="__main__":
    print("-----Hyper Connect Core-----")
    t1 = threading.Thread(target=broadcast_presence, daemon=True)
    t1.start()
    start_data_listener()

