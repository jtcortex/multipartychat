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

import sys,random,hashlib,binascii,os
import re
import xchat

# Crypto Libraries
from M2Crypto import EC
from M2Crypto import BIO
from charm.toolbox.eccurve import prime192v2
from charm.toolbox.ecgroup import ECGroup
from charm.toolbox.PKEnc import PKEnc
from charm.toolbox.ecgroup import G

debug = False
# State Module
from transition import *

def Broadcast(participants, msg=None):
	
	for y in participants:
		if msg == None:
			if not xchat.nickcmp(y.nick, xchat.get_prefs("irc_nick1")) == 0:
				xchat.command("msg " + y.nick + " " + "!Initiate!")
		else:
			if not xchat.nickcmp(y.nick, xchat.get_prefs("irc_nick1")) == 0:
				xchat.command("msg " + y.nick + " " + msg)
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

	z = [y for x,y in connection.usermap.items()]
	z.sort()
	z = "".join(z)
	hash_object = hashlib.sha256(z)
	hex_dig = hash_object.hexdigest()
	connection.session_id = hex_dig
	result,R = DSKE(connection, connection.session_id, participants, 0)
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
	randnum = str.encode(str(r))
	connection.usermap.update({xchat.get_prefs("irc_nick1"):randnum})
	new_randnum = "!c_" + randnum

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

def DSKE(connection, sid, participants, phase=None):
	""" Generate ECDH Keypair and perform an EC El-Gamal exchange with all other participants """
	if phase == 0:
		keypair = EC_GenerateKey(415)
#	path = "/home/jt/Documents/mpOTR-Masters/code/Mpotr/key.pem"
		private_pem = EC_Private(keypair)
		public_pem = EC_Public(keypair)
		z = EC.load_pub_key_bio(BIO.MemoryBuffer(public_pem))
		print "BIO", z
		public_bin = ec_to_public_bin(keypair)
		print "BIN", public_bin.encode("HEX")
		connection.keytable.update({xchat.get_prefs("irc_nick1"):public_bin.encode("HEX")})
		Broadcast(participants, SendKey(public_bin.encode("HEX")))
	if phase == 1:
		pubkeys = [y for x,y in connection.keytable.items()]
 	       	pubkeys.sort()
		pubkeys = "".join(pubkeys)
	        hash_object = hashlib.sha256(pubkeys)
        	hex_dig = hash_object.hexdigest()
		print hex_dig
		Broadcast(participants, SendAssociation(hex_dig))


#	ashared = keypair2.compute_dh_key(keypair.pub())
#	bshared = keypair2.compute_dh_key(z.pub())
	#keypair_one.save_key(path, None)
	#secretkey = KeyExtract(path)
	#print "Secret key: ", secretkey
	#print "newpub", keypair_one.get_der
	#keypair_one.save_pub_key(path2)
	#publickey = KeyExtract(path2)
	#akey = keypair_two.compute_dh_key(keypair_one.pub())
#	bkey = keypair2.compute_dh_key(publickey)
	#if akey == bkey:
	#	print "YEEES"
	#else:
	#	print "NOO"


#	groupObj = ECGroup(prime192v2)
#	el = ElGamal(groupObj)
#	print "SIZE", groupObj.bitsize()
#	x = len(secretkey)/groupObj.bitsize()
#	print "Num MessageS", x
#	for count in range(0,x):

		
#	(public_key, secret_key) = el.keygen()
#	msg = secretkey
#	cipher_text = el.encrypt(public_key,msg)
#	print "CIPHER: ", cipher_text

#	a_shared_key = keypair_one.compute_dh_key(keypair_two.pub())
#	b_shared_key = keypair_two.compute_dh_key(keypair_one.pub())
#	print "A", binascii.b2a_base64(a_shared_key)
#	print "B", binascii.b2a_base64(b_shared_key)
	return (1,0)
		
#def Attest(sid, participants, params):
#''' Authenticate (previously) unauthenticated protocol parameters
#for the current session in the context of party X
#'''
#	M = H(sid, paramts)
#	AuthSend(M)
	

#def AuthUser(sid, B, signature):

def SendAssociation(hashval):

	prefix = b"0x12"
	msg = prefix + hashval
	return msg

def SendKey(key):

	msg = b"0x0a".decode("base64")
	#msg = msg + binascii.b2a_base64(key)
	msg = msg + key
	return msg

def KeyExtract(path):
	
	f = open(path, 'r')
	key = ""
	for line in f:
		if not re.search('-----', line):
			key = key + line
	return key

def EC_GenerateKey(size):
	"""
	Generate Elliptic Curve object with public/private keypair 

	Default security level for curve is 415
	@param size: Level of security
	@type size: Integer
	"""
	assert isinstance(size, int)
	ec = EC.gen_params(size)
	ec.gen_key()
	return ec

def EC_Private(ec, cipher=None, password=None):
	
	def get_password(*args):
		return password or ""
	bio = BIO.MemoryBuffer()
	ec.save_key_bio(bio, cipher, get_password)
	return bio.read_all()

def EC_Public(ec):
	
	bio = BIO.MemoryBuffer()
	ec.save_pub_key_bio(bio)
	return bio.read_all()

def ec_to_public_bin(ec):
	"Get the public key in binary format."
        return ec_public_pem_to_public_bin(EC_Public(ec))	

def ec_public_pem_to_public_bin(pem):
        "Convert a public key in PEM format into a public key in binary format."
        return "".join(pem.split("\n")[1:-2]).decode("BASE64")


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


class ElGamal(PKEnc):

	def __init__(self, groupObj, p=0, q=0):
       		PKEnc.__init__(self)
        	global group
        	group = groupObj
        	if group.groupSetting() == 'integer':
            		group.p, group.q, group.r = p, q, 2

    	def keygen(self, secparam=1024):
		global debug
        	if group.groupSetting() == 'integer':
            		if group.p == 0 or group.q == 0:
                		group.paramgen(secparam)
            		g = group.randomGen()
        	elif group.groupSetting() == 'elliptic_curve':
            		g = group.random(G)
        	# x is private, g is public param
        	x = group.random(); h = g ** x
        	if debug:
            		print('Public parameters...')
            		print('h => %s' % h)
           		print('g => %s' % g)
            		print('Secret key...')
            		print('x => %s' % x)
        	pk = {'g':g, 'h':h }
        	sk = {'x':x}
        	return (pk, sk)

   	def encrypt(self, pk, M):
        	y = group.random()
        	c1 = pk['g'] ** y 
        	s = pk['h'] ** y
        	# check M and make sure it's right size
        	c2 = group.encode(M) * s
        	return ElGamalCipher({'c1':c1, 'c2':c2})

    	def decrypt(self, pk, sk, c):
		global debug
        	s = c['c1'] ** sk['x']
        	m = c['c2'] * (s ** -1)
        	if group.groupSetting() == 'integer':
            		M = group.decode(m % group.p)
        	elif group.groupSetting() == 'elliptic_curve':
            		M = group.decode(m)
        	if debug: print('m => %s' % m)
        	if debug: print('dec M => %s' % M)
        	return M

class ElGamalCipher(dict):
	def __init__(self, ct):
        	if type(ct) != dict: assert False, "Not a dictionary!"
        	if not set(ct).issubset(['c1', 'c2']): assert False, "'c1','c2' keys not present."
        	dict.__init__(self, ct)

    	def __add__(self, other):
        	if type(other) == int:
           		lhs_c1 = dict.__getitem__(self, 'c1')
           		lhs_c2 = dict.__getitem__(self, 'c2')
           		return ElGamalCipher({'c1':lhs_c1, 'c2':lhs_c2 + other})
        	else:
           		pass 

    	def __mul__(self, other):
        	if type(other) == int:
           		lhs_c1 = dict.__getitem__(self, 'c1')
           		lhs_c2 = dict.__getitem__(self, 'c2')
           		return ElGamalCipher({'c1':lhs_c1, 'c2':lhs_c2 * other})
        	else:
           		lhs_c1 = dict.__getitem__(self, 'c1') 
           		rhs_c1 = dict.__getitem__(other, 'c1')

           		lhs_c2 = dict.__getitem__(self, 'c2') 
           		rhs_c2 = dict.__getitem__(other, 'c2')
          		return ElGamalCipher({'c1':lhs_c1 * rhs_c1, 'c2':lhs_c2 * rhs_c2})
       		return None
