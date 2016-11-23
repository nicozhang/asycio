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


def case1():
	s = create_echo_tcp_client();
	s.sendall("hello")
	data = s.recv(1024)
	assert(data == "hello")
	s.close()
