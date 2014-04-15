
# simulation.py
# Module to simulate many users over mpOTR protocol

import Queue, random, multiprocessing
from multiprocessing import Process


class Simulation():
	def __init__(self):
		self.q = Queue.Queue()
		self.users = 4.0
		self.userlist = []
		pass
		
	def Start(self):
		
		server = Server()
		for u in range(0, self.users):
			user = User()
			user.responseProb = 1.0/self.users
			self.userlist.append(user)
		
		
		self.userlist[0].setup(self)
		

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
		self.responseProb = None

	def setup(self, sim):
		self.Broadcast(sim.users, "hey")
		
	def Broadcast(self, participants, msg):
		print msg

def test():
	print "Hello world"

def main():
	sim = Simulation()
	sim.Start()

if __name__ == '__main__':
	main()
		
