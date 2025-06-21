import socket

def math_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    server_ip = input("Enter Math Server IP: ")
    server_port = 12345

    while True:
        nums = input("Enter two numbers separated by space (or 'q' to quit): ")
        if nums.lower() == 'q':
            break
        s.sendto(nums.encode(), (server_ip, server_port))
        data, _ = s.recvfrom(1024)
        print("Server:", data.decode())

if __name__ == "__main__":
    math_client()
