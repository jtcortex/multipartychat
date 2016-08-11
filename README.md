# Encrypted chat plugin

This IRC plugin allows for a side conversation to be started between the requester and a member of the IRC channel. IRC is a known, widely used plaintext protocol and this allows for an easy-to-use method of starting a secure, deniable converation between two parties. This is particularly useful when a potentially untrusted distribution medium (i.e. IRC server) is involved in the communication channel. Users can pose challenge questions at any time during the conversation and can disconnect if it is determined to be unsecure. 

## Dependencies
* M2Crypto

## Usage

* /crypto -r [username]: request a session with [username]
* /crypto -k: reveal session keys for validation
* /crypto -h: display help 
* /crypto -a [question]: ask a question to other party to verify identity
* /crypto -s [path-to-filename]: send a file to the other party


