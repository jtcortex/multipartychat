
# simulation.py
# Module to simulate users over chat

import Queue, random, multiprocessing, socket, time, crypto
from multiprocessing import Process
from multiprocessing.dummy import Pool as ThreadPool
		
class Simulation():
	def __init__(self):
		self.q = Queue.Queue()
		self.users = 4.0
		self.userlist = []
		
	def Start(self):
		
		self.server = Server()
		for u in range(0, int(self.users)):
			user = User("user"+str(u))
			user.responseProb = 1.0/self.users
			self.userlist.append(user)
		
		self.userlist[0].setup(self)
		
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

def test(nick):
	irc = 	'10.8.0.86'
	port = 6667
	channel = '#test'
	sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sck.connect((irc, port))
	sck.send('NICK ' + nick + '\r\n')
	sck.send('USER supaBOT hostname supaBOT :guy Script\r\n')
	sck.send('JOIN #test' + '\r\n')
	data = ''
	while True:
		data = sck.recv(4096)
		print data
		if data.find('PING') != -1:
			sck.send('PONG ' + data.split() [1] + '\r\n')
		if data.find('?mpOTR?') != -1:
			sck.send('PRIVMSG ' + 'carol' + ' :!mpOTR!' + '\r\n')
		if data.find(':!c_') != -1:
			print "GOT IT"
	print sck.recv(4096)

def main():
#	pool = ThreadPool(4)
	#sim = Simulation()
	procs = []
	for i in range(3):
		nick = 'user'+str(i)
		procs.append(multiprocessing.Process(target=test, args=[nick]))
		
	for proc in procs:
		proc.start()
		time.sleep(1)
	#[proc.start() for proc in procs]
	#test('simon')

	#sim.Start()

if __name__ == '__main__':
	main()

	
	


