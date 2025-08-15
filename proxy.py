from socket import *
from urllib.parse import urlparse
import sys
import os

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : The IP Address of the Proxy Server]')
    sys.exit(2)

# Create server socket, bind it, and listen
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerPort = 60003
tcpSerSock.bind(('', tcpSerPort))
tcpSerSock.listen(10)
print("Proxy server is running on port", tcpSerPort)

while True:
    print('\nReady to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    try:
        message = tcpCliSock.recv(4096).decode()
        if not message:
            tcpCliSock.close()
            continue

        print("Request message:\n", message)

        # Parse the first line
        request_line = message.splitlines()[0]
        print("Request line:", request_line)
        method, url, protocol = request_line.split()

        # Only support GET
        if method != "GET":
            print("Unsupported method:", method)
            tcpCliSock.send("HTTP/1.0 405 Method Not Allowed\r\n\r\n".encode())
            tcpCliSock.close()
            continue

        # Parse the URL
        parsed_url = urlparse(url)
        hostn = parsed_url.hostname
        port = parsed_url.port or 80
        path = parsed_url.path or "/"

        print("Host:", hostn)
        print("Path:", path)

        # File name to use in cache
        filename = hostn + path
        filename = filename.replace("/", "_")
        filetouse = "./cache/" + filename

        fileExist = os.path.isfile(filetouse)

        if fileExist:
            # Cache hit
            print("Cache hit:", filetouse)
            with open(filetouse, "rb") as f:
                cached_data = f.read()
                tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
                tcpCliSock.send(b"Content-Type: text/html\r\n\r\n")
                tcpCliSock.send(cached_data)
        else:
            # Cache miss: connect to remote server
            print("Cache miss. Connecting to", hostn)

            c = socket(AF_INET, SOCK_STREAM)
            c.connect((hostn, port))

            request = f"GET {path} HTTP/1.0\r\nHost: {hostn}\r\n\r\n"
            c.send(request.encode())

            if not os.path.exists("./cache"):
                os.mkdir("./cache")

            with open(filetouse, "wb") as tmpFile:
                while True:
                    buff = c.recv(4096)
                    if not buff:
                        break
                    tmpFile.write(buff)
                    tcpCliSock.send(buff)

            c.close()

    except Exception as e:
        print("Error:", e)
        tcpCliSock.send("HTTP/1.0 500 Internal Server Error\r\n\r\n".encode())
    finally:
        tcpCliSock.close()
