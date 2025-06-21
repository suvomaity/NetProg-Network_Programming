import socket

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  
    SERVER_IP = '192.168.0.155'  # your actual IP
    PORT = 12345

    s.bind((SERVER_IP, PORT))
    print(f"Server started on {SERVER_IP}:{PORT}")

    while True:
        data, addr = s.recvfrom(1024)
        print(f"Received from {addr}: {data.decode()}")
        s.sendto(f"Echo: {data.decode()}".encode(), addr)

if __name__ == "__main__":
    server()
