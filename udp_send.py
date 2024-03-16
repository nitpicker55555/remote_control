import socket

# Set up the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the target IP and port
target_ip = '10.181.210.246'  # Assuming localhost for now. Change this to your target IP.
target_port = 8888

# Message to be sent
message = "Hello, UDP Server!"

try:
    # Send the message
    sock.sendto(message.encode(), (target_ip, target_port))
    print(f"Sent message: {message} to {target_ip}:{target_port}")

finally:
    sock.close()
