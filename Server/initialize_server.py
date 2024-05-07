from server import register_at_coordinator

port = 10000
for i in range(0,100):
    ip = "192.168.0." + str(i)
    register_at_coordinator(ip, port)