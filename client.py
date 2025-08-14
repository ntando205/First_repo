import socket

s = socket.socket()
host = socket.gethostname()
port = 6000

s.connect((host, port))
s.send(b'Hello Server!')

with open('received_file', 'wb') as f:
    print("File opened")

    while True:
        print("Receiving data...")
        data = s.recv(1024)
        print("data=%s", (data))

        if not data:
            break

        # write data to a file
        f.write(data)

    f.close()
print("Successfully got the file")
s.close()

print("Connection closed")
