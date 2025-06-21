import socket

def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    SERVER_IP = input("Enter Server IP address : ")
    PORT = 12345

    while True:
        msg = input("Message (q to quit): ")
        if msg == 'q':
            break
        s.sendto(msg.encode(), (SERVER_IP, PORT))
        data, _ = s.recvfrom(1024)
        print("Reply:", data.decode())

if __name__ == "__main__":
    client()
