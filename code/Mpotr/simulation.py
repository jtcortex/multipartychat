
# simulation.py
# Module to simulate many users over mpOTR protocol

import Queue, random, multiprocessing
from multiprocessing import Process


class Simulation():
	def __init__(self):
		self.q = Queue.Queue()
		self.users = 4
		self.userlist = []
		pass
		
	def Start(self):
		
		server = Server()
		for u in range(0, self.users):
			user = User()
			self.userlist.append(user)
		
		
		self.userlist[0].setup()
		

class Server():
	def __init__(self):
		q = Queue.Queue()
		pass

	def relay(self, receive, send):
		pass
	
class Message():

	def __init__(self):
		msgLength = random.randint(2, 200) #length of the message in bytes
		
class User():
	def __init__(self):
		self.distance = random.randrange(20, 400)

	def setup(self):
		print "YESS"

def test():
	print "Hello world"

def main():
	sim = Simulation()
	sim.Start()

if __name__ == '__main__':
	main()
		
