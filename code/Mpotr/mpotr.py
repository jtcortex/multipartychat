#!/usr/bin/env python
'''
 * Multi-Party Off-The-Record Messaging (Experimental)
 *
 * Author: James Corcoran
 * Computer Engineering and Computer Science Dept
 * JB Speed School of Engineering
 * University of Louisville, KY, USA
 *
 * Based on the work of Goldberg, et. al.
'''

import sys,random,hashlib,threading
import xchat

# Crypto Libraries
from M2Crypto import EC
#from charm.toolbox.eccurve import prime256v1
#from charm.toolbox.ecgroup import ECGroup
from transition import *

def Broadcast(participants, msg=None):
	
	for y in participants:
		if msg == None:
			if not xchat.nickcmp(y.nick, xchat.get_prefs("irc_nick1")) == 0:
				xchat.command("msg " + y.nick + " " + "!Initiate!")
		else:
			if not xchat.nickcmp(y.nick, xchat.get_prefs("irc_nick1")) == 0:
				xchat.command("msg " + y.nick + " " + "!c_" + msg)
	return xchat.EAT_ALL

def Initiate(connection, participants, sender=None):
	''' Initiate a chatroom C among the participants P in the context of
	party X. On successful completion, all participants hold a shared 
	encryption key, epheremal public signature keys for all other 
	participants, and have authenticated all other participants and 
	protocol parameters. 
	'''
	session_id = None
	sent = 0 
	received = 0
	consensus = []
	Broadcast(participants)
	CreateSession(participants, connection)
#		consensus[y] = 0

def ContInitiate(connection, participants):

	print "MADE TO CONTININT"
	z = [y for x,y in connection.usermap.items()]
	z.sort()
	z = "".join(z)
	print z
	hash_object = hashlib.sha256(z)
	hex_dig = hash_object.hexdigest()
	connection.session_id = hex_dig
	result,R = DSKE(connection.session_id, participants)
	print "RESULT", result
	print "R", R
#	if result == 1:
#		for E,Y in R:
#			assign()
#	else:
#		Abort()

#	groupKey = GKA(participants, R)
#	if gk == None:
#		Abort()
#	Attest()

def CreateSession(participants, connection):
	''' Invoked in the context of party X, the algorithm returns a 
	unique (with high probability) chatroom identifier for the set
	P upon successful completion 
	'''
	r = random.getrandbits(128)
	new_randnum = str.encode(str(r))
	connection.usermap.update({xchat.get_prefs("irc_nick1"):new_randnum})

	Broadcast(participants, new_randnum)

#	--- This may be needed later, but locally there is no delay ---
#	while (Receive_Participants(participants, connection) == 0):
#		pass
	#th1 = threading.Thread(target=Receive_Participants, args=(participants, connection))
	#th1.start()
	
#	newlist = sorted(connection.usermap.values())
#	print "Newlist", newlist
#	hash_object = hashlib.sha256(new_str)
#	hex_dig = hash_object.hexdigest()
#	print(hex_dig)
#	x = BinaryString()
#	keypair_one = EC.gen_params(415)
#	keypair_one.gen_key()
#	keypair_two = EC.gen_params(415)	
#	keypair_two.gen_key()
#	a_shared_key = keypair_one.compute_dh_key(keypair_two.pub())
#	b_shared_key = keypair_two.compute_dh_key(keypair_one.pub())

#	f = open('/home/sojiro/Documents/Project/outfile.dat', 'w')
#	f.write("PRIVATE KEY")
#	f.write(keypair_one.priv())
#	f.write("A SHARED KEY: ")
#	f.write(a_shared_key)
#	f.write("B SHARED KEY: ")
#	f.write(b_shared_key)
#	outstanding = P\X
#	while outstanding != 0:

def DSKE(sid, participants):
	return (1,0)
		
#def Attest(sid, participants, params):
#''' Authenticate (previously) unauthenticated protocol parameters
#for the current session in the context of party X
#'''
#	M = H(sid, paramts)
#	AuthSend(M)
	

#def AuthUser(sid, B, signature):



#def AuthSend(M, sid, gk, ex):
''' Broadcast message M authenticated under party X's epheremal 
signing key to chatroom C
'''
#	sent = sent + M
#	C = Encrypt(M) 
#	sigma = Sign(sid, C)
#	Broadcast(sid, C, sigma)

#def AuthReceive(sid, gk, )


#def Shutdown(


