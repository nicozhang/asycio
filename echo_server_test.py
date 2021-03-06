#!/usr/bin/python

import socket
import os

def setup():
	os.system("./echo_server.py &")
	os.system("sleep 1")

def teardown():
	os.system("sleep 1")
	os.system("killall echo_server.py")

def create_echo_tcp_client():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	s.connect(("127.0.0.1", 8080))
	return s


def test_send_reply():
	s = create_echo_tcp_client()
	s.sendall("hello")
	data = s.recv(1024)
	assert(data == "hello")
	s.close()

def test_send_large_data():
	s = create_echo_tcp_client()

	data = ""
	for idx in range(0, 10000):
		data = data + 'A'

	s.sendall(data);
	received = s.recv(10000)

	assert(data == received)
	s.close()
