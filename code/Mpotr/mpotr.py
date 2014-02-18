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

import sys,random
import xchat
from M2Crypto import EC

def Initiate(participants):
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
	for y in participants:
		print y.nick
#		consensus[y] = 0

	session_id = SessionID(participants)
#	result,R = DSKE(session_id, participants)
#	if result == 1:
#		for E,Y in R:
#			assign()
#	else:
#		Abort()

#	groupKey = GKA(participants, R)
#	if gk == None:
#		Abort()
#	Attest()

def SessionID(participants):
	''' Invoked in the context of party X, the algorithm returns a 
	unique (with high probability) chatroom identifier for the set
	P upon successful completion 
	'''
#	x = BinaryString()
	keypair_one = EC.gen_params(415)
	keypair_one.gen_key()
	keypair_two = EC.gen_params(415)	
	keypair_two.gen_key()
	a_shared_key = keypair_one.compute_dh_key(keypair_two.pub())
	b_shared_key = keypair_two.compute_dh_key(keypair_one.pub())
	f = open('/home/sojiro/Documents/Project/outfile.dat', 'w')
	f.write("PRIVATE KEY")
	f.write(keypair_one.priv())
#	f.write("A SHARED KEY: ")
#	f.write(a_shared_key)
#	f.write("B SHARED KEY: ")
#	f.write(b_shared_key)
#	outstanding = P\X
#	while outstanding != 0:
		




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


