import socket

HOST = "192.168.4.152" 
# HOST = "172.20.10.3"
PORT = 8080

def askServer(string):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(string.encode())
        data = s.recv(1024)
    data = data.decode('ascii')
    print(f"received {data} successfully")
    return data
