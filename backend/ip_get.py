import socket

hostname = socket.gethostname()
ips = socket.getaddrinfo(hostname, None)

ipv4s = list({item[4][0] for item in ips if "." in item[4][0]})

print(ipv4s)
