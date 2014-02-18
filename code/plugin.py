
'''
 * Multi-Party Off-The-Record Messaging Plugin (Experimental)
 *
 * Author: James Corcoran
 * Computer Engineering and Computer Science Dept
 * JB Speed School of Engineering
 * University of Louisville, KY, USA
 *
 * Based on the work of Goldberg, et. al.
'''

__module_name__ = "plugin"
__module_version__ = "0.1"
__module_description__ = "X-Chat mpOTR plugin"

# Plugin/System/Crypto packages
import xchat,sys,re
import M2Crypto

# Ammend system path to include mpOTR library
sys.path.append("/home/sojiro/Documents/Project/Mpotr")
import mpotr

## Some global variables for the script
SENDER = ""
INVITE = 0
acceptlist = []
userlist = []

def broadcast(users, p2p):
	''' Send a message to all users in a channel '''
	for x in users:
		if not xchat.nickcmp(x.nick, xchat.get_prefs("irc_nick1")) == 0:
			xchat.command("msg " + x.nick + " " + "?mpOTR?")
	return xchat.EAT_ALL
		

def mpotr_cb(word, word_eol, userdata):
	''' Callback for /mpotr command '''
	if len(word) < 2:
		print "Second arg must be the action!"
		print "\nAvailable actions:"
		print "     auth - initiate mpOTR session and authenticate participants"
	elif word[1] == "auth":
		setup()
		if '-p2p' in word_eol:
			broadcast(xchat.get_list("users"), 1)
		else:
			broadcast(xchat.get_list("users"), 0)
	elif word[1] == "y":
		print "SENDER", SENDER
		xchat.command("msg " + SENDER + " " + "!mpOTR!")
	else:
		xchat.prnt("Unknown action")
	return xchat.EAT_ALL

def say_cb(word, word_eol, userdata):
	''' Word Interception'''
	return xchat.EAT_ALL

def msg_cb(word, word_eol, userdata):
	global SENDER
	global INVITE
	global acceptlist
	if ":?mpOTR?" in word:
		sender = re.search('(?<=:)\w+', word[0])
		SENDER = sender.group(0)
		INVITE = 1
		print SENDER, "wishes to take this conversation off the record. Do you accept?"
	elif ":!mpOTR!" in word:
		sender = re.search('(?<=:)\w+', word[0])
		SENDER = sender.group(0)
		for user in acceptlist:
			if SENDER == user[0].nick:
				user[1] = 1
		if allAccept() == 1:
			mpotr.Initiate(userlist)
	return xchat.EAT_ALL

def setup():

	global acceptlist
	global userlist
	acceptlist = []
	userlist = xchat.get_list("users")
	for x in userlist:
		if xchat.nickcmp(x.nick, xchat.get_prefs("irc_nick1")) == 0:
			acceptlist.append([x, 1])
		else:
			acceptlist.append([x, 0])

def allAccept():
	
	global acceptlist
	size = len(acceptlist)
	count = 0
	for x in acceptlist:
		if x[1] == 1:
			count = count + 1
	if count == size:
		return 1
	else:
		return 0

xchat.hook_print("Your Message", say_cb)
xchat.hook_print("Message send", say_cb)
#xchat.hook_print("Private Message", say_cb)
xchat.hook_server("PRIVMSG", msg_cb)
xchat.hook_command("MPOTR", mpotr_cb, help="/MPOTR <action> Performs mpOTR action for channel participants")
