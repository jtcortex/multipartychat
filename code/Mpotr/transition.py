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
		self.usermap = {}
		self.keytable = {}

	def SetUsers(self, users):
		self.users = users

	def SetState(self, state):
		self.currentState = state
		if state == "ContInitiate":
			mpotr.ContInitiate(self, self.users)
		elif state == "DSKE":
			mpotr.DSKE(self, self.session_id, self.users, 1)
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
