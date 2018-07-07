import socket

target_host = "127.0.0.1"
target_port = 9999
# payload = "GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n"
# payload = payload.encode('utf-8')
payload = 'Hi'
payload = payload.encode('UTF-8')

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_host, target_port))
    s.send(payload)
    response = s.recv(4096)
    print(response.decode())

except ConnectionRefusedError:
    print("Connection failed... Verify target information.")
    exit()
