import socket
import select


def createTcpServer(host, port):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	server.bind((host, port))
	server.listen(10)
	
	return server

connections = []
read = []
read_action = {}
read_repeats = {}
write = []
write_action = {}
write_repeats = {}

def onAccept(server, func, repeat = 1):

		read.append(server)
		connections.append(server)
		read_repeats[server.fileno()] = repeat
		
		def onAccept_cb():
			c, addr = server.accept()
			connections.append(c)
			func(c, addr)
			
		read_action[server.fileno()] = onAccept_cb
	
def onRecv(sock, func, repeat = 0):
	read.append(sock)
	read_repeats[sock.fileno()] = repeat
	
	def onRecv_cb():
		print "Recevi new data"
		data = sock.recv(1024)
		func(sock, data)
		
	read_action[sock.fileno()] = onRecv_cb
	
def onSend(sock, data, func):
		write.append(sock)
		write_repeats[sock.fileno()] = 0
		
		def onSend_cb():
			sock.send(data)
			func(sock)
			
		write_action[sock.fileno()] = onSend_cb

	
def send_data(sock):
	onRecv(sock, receiv_new_data)
	
def receiv_new_data(sock, data):
		print sock, "recv:", data
		onSend(sock, data, send_data)
	
def accept_new_client(client, addr):
		print "Receive a new client", addr
		onRecv(client, receiv_new_data)

		

def run_loop():
			while True:
			
				r, w, e = select.select(read, write, [])
				for sock in connections:
						if sock in r:
							func = read_action[sock.fileno()]
							func()
							if read_repeats[sock.fileno()] == 0:
								read.remove(sock)
								del(read_action[sock.fileno()])
								del(read_repeats[sock.fileno()])
						elif sock in w:
							func = write_action[sock.fileno()]
							func()
							if write_repeats[sock.fileno()] == 0:
								write.remove(sock)
								del(write_action[sock.fileno()])
								del(write_repeats[sock.fileno()])
				
				
				
s = createTcpServer("0.0.0.0", 8080)
onAccept(s, accept_new_client)

run_loop()
