#! /usr/bin/env python

# transition.py
# State machine for the CRYPTO Connection

import multi, time, thread

class CRYPTOConnection(object):
	""" crypto Connection """
	
	def __init__(self, path, states=[]):
		self._states = states
		self.currentState = None
		self.state = CRYPTOState(self)
#		self.users = users
		self.session_id = None
		self.keyhash = None
		self.usermap = {}
		self.keytable = {}
		self.associationtable = {}
		self.userkeytable = {}
		self.users = []
		self.public_pem = None
		self.private_pem = None
		self.keypair = None
		self.groupkey = None
		self.path = path
		self.digestTable = {}
		self.t0 = ""

	def SetUsers(self, users):
		self.users = users

	def SetInfo(self, server, channel, username):
		self.server = server
		self.channel = channel
		self.username = username

	def SetState(self, state):
		self.currentState = state
		if state == "ContInitiate":
			crypto.Initiate(self, self.users, 1)
		elif state == "DSKE":
			crypto.DSKE(self, self.session_id, self.users, 1)
		elif state == "Verify":
			result = crypto.DSKE(self, self.session_id, self.users, 2)
			print result
			if result == 1:
				crypto.GKA(self, self.keytable, 0)
		elif state == "GROUP_KEY_AUTHENTICATE":
			self.currentState = "GROUP_KEY_AUTHENTICATE"
			crypto.GKA(self, self.keytable, 1)
		elif state == "MSGSTATE_ENCRYPTED":
			self.currentState = "MSGSTATE_ENCRYPTED"
			crypto.BeginLogging(self)
		elif state == "SHUTDOWN_COMPLETE":
			crypto.Send_Epheremal(self)
	def Start(self, startState=None):
		self.currentState = startState
		crypto.Initiate(self, self.users, 0)
	
	def Close(self):
		print "Closed"

	def Send(self):
		print "Send"

	def getUsers(self):
		return self.users

class CRYPTOState(object):
	""" State of crypto Connection """

	def __init__(self, states=[]):
		print "HEY"

	def Setup():
		print "HEY"
