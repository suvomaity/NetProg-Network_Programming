import socket

def math_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', 12345)) 
    print("Math Server is running on port 12345...")

    while True:
        data, addr = s.recvfrom(1024)
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

        s.sendto(response.encode(), addr)

if __name__ == "__main__":
    math_server()
