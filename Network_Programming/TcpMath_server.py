import socket

def math_server_tcp():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen()

    print("TCP Math Server is running on port 12345...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected by {addr}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Connection closed by {addr}")
                break

            try:
                nums = data.decode().strip().split() 
                if len(nums) != 2:
                    response = "Error: Send exactly two numbers"
                else:
                    a, b = float(nums[0]), float(nums[1])
                    result = a + b
                    response = f"Sum = {result}"
            except Exception as e:
                response = f"Error: {str(e)}"

            client_socket.sendall(response.encode())

        client_socket.close()

if __name__ == "__main__":
    math_server_tcp()
