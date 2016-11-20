#!/usr/bin/python

import async_socket
import event_loop
import os

loop = event_loop.select_loop()
s = async_socket.async_tcp_server("127.0.0.1", 8080, loop)

def send_data_finish(client):
	pass

def receive_new_data(client, data):
	client.on_send(data, send_data_finish)	
	

def accept_new_client(client, address):
	print "new client accpet", address
	client.on_recv(receive_new_data)	

s.on_accept(accept_new_client)
loop.run()
