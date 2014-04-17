
# simulation.py
# Module to simulate many users over mpOTR protocol

import Queue, random, multiprocessing
from multiprocessing import Process
from multiprocessing.dummy import Pool as ThreadPool


class Simulation():
	def __init__(self):
		self.q = Queue.Queue()
		self.users = 4.0
		self.userlist = []
		pass
		
	def Start(self):
		
		self.server = Server()
		for u in range(0, int(self.users)):
			user = User("user"+str(u))
			user.responseProb = 1.0/self.users
			self.userlist.append(user)
		
		self.userlist[0].setup(self)
		

class Server():
	def __init__(self):
		self.q = Queue.Queue()
		pass

	def relay(self, receive, send, msg):
		pass

	def check(self, sim):
		while not self.q.empty():
			(x,y) = self.q.get_nowait()
			for user in sim.userlist:
				if not x == user:
		#			this.relay(
					print x
			print y
					

	def Start():
		pass
	
class Message():

	def __init__(self):
		msgLength = random.randint(2, 200) #length of the message in bytes
		
class User(multiprocessing.Process):
	def __init__(self, name):
		self.distance = random.randrange(20, 400)
		self.responseProb = None
		self.q = Queue.Queue()
		self.name = name

	def setup(self, sim):
		self.Broadcast(sim, "0x12user")
		
	def Broadcast(self, sim, msg):
		for p in sim.userlist:
			if not self == p:
				# add messages to server queue
				sim.server.q.put((self, msg))		
		sim.server.check(sim)

	def Receive(self, msg):
		pass

def test():
	print "Hello world"

def main():
#	pool = ThreadPool(4)
	sim = Simulation()
	sim.Start()

if __name__ == '__main__':
	main()


