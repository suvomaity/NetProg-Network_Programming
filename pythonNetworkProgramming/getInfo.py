import socket

name=socket.gethostname()  # Get the local machine name
ip=socket.gethostbyname(name)  # Get the IP address of the local machine

print("Your Computer Name is:" + name)
print("Your Computer IP Address is:" + ip)