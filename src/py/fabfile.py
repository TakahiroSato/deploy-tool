from StringIO import StringIO
from pprint import pprint
from fabric.api import env
from fabric.operations import run, put, get, sudo
from fabric.api import local, lcd
from fabric.contrib import files
import string
import os, re, sys, time
import datetime
import json

try:
  with open('../../data/connections.json', 'r') as f:
    connectionsData = json.load(f)
except json.JSONDecodeError as e:
  print('JSONDecodeError: ', e)

def setHost(settingName):
    for h in filter(lambda c: c['settingName'] == settingName, connectionsData):
      env.hosts = h['host']
      env.key_filename = h['secretKey']
      env.password = h['password']
      env.user = h['userName']
      #env.localRoot = 
      #env.localBackUpRoot = 
      #env.remoteRoot = 
      env.sudo_prompt = '[sudo] password for ' + env.user + ':'

def printEnv():
    pprint(env)

def deploy():
	backup()
	print "start deploy-------------\n"
	start = time.time()
	remoteDir = env.remoteRoot
	f = open(env.file, 'r')
	for file in f:
		file = file.replace('\n','')
		if not ("#" in file) and not (file.isspace()) and len(file) > 0 and file is not None:
			if not files.exists(remoteDir + re.sub(r'\/[^\/]*$', '', file)):
				run('mkdir -p ' + remoteDir + re.sub(r'\/[^\/]*$', '', file))
			put(env.localRoot + file, remoteDir + file)
	print ("elapsed_time:{0}".format(time.time() - start)) + "[sec]"

def backup():
	print "start backup-------------\n"
	start = time.time()
	remoteDir = env.remoteRoot
	err = []
	f = open(env.file, 'r')
	for file in f:
		file = file.replace('\n', '')
		if not ("#" in file) and not (file.isspace()) and len(file) > 0 and file is not None:
			try:
				get(remoteDir + file, env.localBackUpRoot + file)
			except:
				err.append(remoteDir + file)

	local('chmod -R 775 ' + env.localBackUpRoot)
	if len(err) > 0:
		print '\nNot exist files:\n\n========'
		for s in err:
			print printc(s)
		print '========\n\n'
	else:
		print printc('All clear!!!')
	print ("elapsed_time:{0}".format(time.time() - start)) + "[sec]"

	print ("\n\ncommit")
	today = datetime.datetime.today()
	with lcd('./dir'):
		try:
			local('git add -A')
			local('git commit -m "' + str(today) + '"')
		except:
			print("nothing to commit")

