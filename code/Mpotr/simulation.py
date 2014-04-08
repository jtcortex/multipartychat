
# simulation.py
# Module to simulate many users over mpOTR protocol

import Queue, random, mpotr

class User():

	def __init__(self):
		distance = random.randint(15, 250) #random value based on distance of user from server
		
class Server():
	
	def __init__(self):
		serverQueue = Queue.Queue()
	
	
class Message():

	def __init__(self):
		msgLength = random.randint(2, 200) #length of the message
		