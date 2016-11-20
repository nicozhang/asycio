import socket

class async_socket:

	def __init__(self, socket, event_loop):
		self.socket = socket
		self.event_loop = event_loop
		self.event_loop.new_connection(socket)

	def register_read_action(self, func, repeat = 1):
		self.event_loop.register_read_action(self.socket, func, repeat)

	def register_write_action(self, func):
		self.event_loop.register_write_action(self.socket, func)

	def on_recv(self, func, repeat = 1):

        	def onRecv_cb():
                	print "Recevi new data"
                	data = self.socket.recv(1024)
                	func(self, data)

		self.register_read_action(onRecv_cb, repeat)

	def on_send(self, data, func):
		print "prepare to send"		
                def onSend_cb():
			print "sending: ", data
                        self.socket.send(data)
                        func(self)

		self.register_write_action(onSend_cb)

	def on_close(self, func):
		pass


class async_tcp_server(async_socket):
	def __init__(self, address, port, event_loop):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((address, port))
		s.listen(10)

		async_socket.__init__(self, s, event_loop)	

	def on_accept(self, func):

                def onAccept_cb():
                        c, addr = self.socket.accept()
			cs = async_tcp_client(c, self.event_loop)
                        func(cs, addr)

		self.register_read_action(onAccept_cb)


class async_tcp_client(async_socket):
	def __init__(self, socket, event_loop):
		async_socket.__init__(self, socket, event_loop)
