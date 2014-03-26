#! /usr/bin/env python

# transition.py
# State machine for the MPOTR Connection

import mpotr

class MPOTRConnection(object):
	""" mpOTR Connection """

	def __init__(self, states=[]):
		self._states = states
		self.currentState = None
		self.state = MPOTRState(self)
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

	def SetUsers(self, users):
		self.users = users

	def SetState(self, state):
		self.currentState = state
		if state == "ContInitiate":
			mpotr.ContInitiate(self, self.users)
		elif state == "DSKE":
			mpotr.DSKE(self, self.session_id, self.users, 1)
		elif state == "Verify":
			result = mpotr.DSKE(self, self.session_id, self.users, 2)
			print result
			if result == 1:
				mpotr.GKA(self, self.keytable, 0)
		elif state == "MSGSTATE_ENCRYPTED":
			self.currentState = "MSGSTATE_ENCRYPTED"
			mpotr.GKA(self, self.keytable, 1)
	def Start(self, startState=None):
		self.currentState = startState
		mpotr.Initiate(self, self.users)
	
	def Close(self):
		print "Closed"

	def Send(self):
		print "Send"

	def getUsers(self):
		return self.users

class MPOTRState(object):
	""" State of mpOTR Connection """

	def __init__(self, states=[]):
		print "HEY"

	def Setup():
		print "HEY"
