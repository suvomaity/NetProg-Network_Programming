import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(f"\nFrom {addr}: {data.decode()}")
        except:
            break

def chat(my_ip, my_port, peer_ip, peer_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((my_ip, my_port))

    # Start receiving thread
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    print("You can start typing your messages. Type 'q' to quit.")
    while True:
        msg = input()
        if msg == 'q':
            break
        sock.sendto(msg.encode(), (peer_ip, peer_port))

if __name__ == "__main__":
    my_ip = input("Your IP: ")           
    my_port = int(input("Your Port: ")) 

    peer_ip = input("Friend's IP: ")     
    peer_port = int(input("Friend's Port: "))  # 12346

    chat(my_ip, my_port, peer_ip, peer_port)
