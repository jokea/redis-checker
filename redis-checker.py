#!/usr/bin/env python

# Check the data consistency of redis servers.
# Accepts an integer as parameter to specify how many keys to check.

import redis
import sys
import os
import time
from config import *

connections = []
mismatch_set = set()

def connect_all() :
	for server in servers :
		tmp = server.partition(':')
		ip = tmp[0]
		port = int(tmp[2])
		r = redis.Redis(ip, port, 0)
		connections.append(r)

def check(key, type) :
	first = None
	for r in connections :
		if type == 'string' :
			value = r.get(key)
		elif type == 'list' :
			value = r.lrange(key, 0, -1)
		elif type == 'hash' :
			value = r.hgetall(key)
		elif type == 'set' :
			value = r.smembers(key)
		elif type == 'zset' :
			value = r.zrange(key, 0, -1)
		elif type == 'none' :
			return
		else :
			return

		if first == None :
			first = value
		else :
			if value != first :
				mismatch_set.add(key)
				return

def main() :
	connect_all()
	r = connections[0]
	if len(sys.argv) == 1 :
		count = 1
	else :
		count = long(sys.argv[1])
	
	for i in xrange(0, count) :
		time.sleep(interval)
		key = r.randomkey()
		if key :
			type = r.type(key)
			check(key, type)

	print 'Total mismatches', len(mismatch_set)
	for x in mismatch_set :
		print x


if __name__ == '__main__' :
	main()
