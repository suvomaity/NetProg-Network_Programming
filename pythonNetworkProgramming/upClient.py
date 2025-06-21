import socket

# Server function
def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('192.168.0.156', 12345))
    print("Server started on port 12345")
    while True:
        data, addr = s.recvfrom(1024)
        print("Received:", data.decode())
        s.sendto(f"Echo: {data.decode()}".encode(), addr)

# Client function
def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        msg = input("Message (q to quit): ")
        if msg == 'q':
            break
        s.sendto(msg.encode(), ('192.168.0.156', 12345))
        data, _ = s.recvfrom(1024)
        print("Reply:", data.decode()) 

# Main
if input("Run (s)erver or (c)lient? ") == 's':
    server()
else:
    client()
