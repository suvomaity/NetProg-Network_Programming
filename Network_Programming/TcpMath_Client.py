import socket

def math_client_tcp():
    server_ip = input("Enter Math Server IP : ")
    server_port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        print("Connected to the server.")

        while True:
            nums = input("Enter two numbers separated by space (or 'q' to quit): ")
            if nums.lower() == 'q':
                break
            s.sendall(nums.encode())
            data = s.recv(1024)
            print("Server:", data.decode())

if __name__ == "__main__":
    math_client_tcp() 
