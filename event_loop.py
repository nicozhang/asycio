import socket
import async_socket
import select

class event_loop:
	def run(self):
		pass

class select_loop(event_loop):

	def __init__(self):
		self.connections = []
		self.read = []
		self.read_action = {}
		self.read_repeats = {}
		self.write = []
		self.write_action = {}

	def new_connection(self, sock):
		self.connections.append(sock)	

	def del_connection(self, sock):
		self.connections.remove(sock)
		self.read.remove(sock)
		self.write.remove(sock)
		self.read_action.remove(sock.fileno())
		self.read_repeats.remove(sock.fileno())	
		self.write_action.remove(sock.fileno())

	def register_read_action(self, sock, func, repeat = 1):
		self.read.append(sock)
		self.read_action[sock.fileno()] = func
		self.read_repeats[sock.fileno()] = repeat

	def register_write_action(self, sock, func):
		self.write.append(sock)
		self.write_action[sock.fileno()] = func

	def run(self):
		while True:
			r, w, e = select.select(self.read, self.write, [])
			for sock in self.connections:
				if sock in r:
					func = self.read_action[sock.fileno()]
					func()
					if self.read_repeats[sock.fileno()] == 0:
						self.read.remove(sock)
						del(self.read_action[sock.fileno()])
						del(self.read_repeats[sock.fileno()])

				if sock in w:
					func = self.write_action[sock.fileno()]
					func()
					self.write.remove(sock)
					del(self.write_action[sock.fileno()])
