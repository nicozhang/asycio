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
		print "new sock fd = ", sock.fileno()

	def del_connection(self, sock):
		print "del sock fd = ", sock.fileno()
		self.connections.remove(sock)
		if sock in self.read:
			self.read.remove(sock)
			del self.read_action[sock.fileno()]
			del self.read_repeats[sock.fileno()]

		if sock in self.write:
			self.write.remove(sock)
			del self.write_action[sock.fileno()]

	def register_read_action(self, sock, func, repeat = 1):
		self.read.append(sock)
		self.read_action[sock.fileno()] = func
		self.read_repeats[sock.fileno()] = repeat

	def register_write_action(self, sock, func):
		if self.write_action.get(sock.fileno()) is None:
			self.write_action[sock.fileno()] = [func]
			self.write.append(sock)
		else:
			self.write_action[sock.fileno()].append(func)

	def run(self):
		while True:
			r, w, e = select.select(self.read, self.write, [])
			print "Read socket:"
			print self.read
			for sock in r:
				func = self.read_action.get(sock.fileno())
				if func is None:
					continue

				func()
				print sock
				if self.read_repeats[sock.fileno()] == 0:
					self.read.remove(sock)
					del(self.read_action[sock.fileno()])
					del(self.read_repeats[sock.fileno()])

			for sock in w:
				func_list = self.write_action.get(sock.fileno())
				
				if func_list is None:
					continue

				print "len (func_list) = ", len(func_list)
				if len(func_list) == 1:
					self.write.remove(sock)
					del(self.write_action[sock.fileno()])

				func = func_list.pop(0)
				func()
