#!/bin/bash
rm mpotr_plugin.o
rm mpotr_plugin.so
rm /usr/lib/weechat/plugins/mpotr_plugin.so
gcc -fPIC -Wall -c mpotr_plugin.c
gcc -shared -fPIC -o mpotr_plugin.so mpotr_plugin.o

cp mpotr_plugin.so /usr/lib/weechat/plugins
