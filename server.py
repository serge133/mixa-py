import socket

HOST = "192.168.4.152"
# HOST = "172.20.10.3"
print(HOST)
PORT = 8080

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()

        with conn:
            print(f'Connected by {addr}')
            while True:
                data = conn.recv(1024)
                if not data:
                    break 
                try:
                    string = str((data.decode('utf-8')).strip())
                    print("Recieved: ", string)
                    # determine_action(string=string)
                    conn.sendall(b"SUCCESS!")
                except:
                    conn.sendall(b"FAILED!")
                # conn.sendall(string.encode())