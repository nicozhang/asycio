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

	def register_read_action(self, sock, func, repeat = 1):
		print "register_read_action", sock, func
		self.read.append(sock)
		self.read_action[sock.fileno()] = func
		self.read_repeats[sock.fileno()] = repeat

	def register_write_action(self, sock, func):
		print "register_write_action", sock, func
		self.write.append(sock)
		self.write_action[sock.fileno()] = func

	def run(self):
		while True:
			r, w, e = select.select(self.read, self.write, [])
			print "read: ", r
			print "write: ", w
			print "connections: ", self.connections
			for sock in self.connections:
				if sock in r:
					func = self.read_action[sock.fileno()]
					func()
					if self.read_repeats[sock.fileno()] == 0:
						self.read.remove(sock)
						del(self.read_action[sock.fileno()])
						del(self.read_repeats[sock.fileno()])

				if sock in w:
					print "Can write"
					func = self.write_action[sock.fileno()]
					func()
					self.write.remove(sock)
					del(self.write_action[sock.fileno()])
