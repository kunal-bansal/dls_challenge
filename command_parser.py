"""
Handles the work of validating and processing command input.
"""

import subprocess
import time
import math

from sqlalchemy import exists

from base import Command
from db import session

import os
import signal

def get_valid_commands(queue, filename):
    # TODO: efficiently evaluate commands from filename passed
    # queue.put(command)
    valid_commands = set()
    commands = set()
    flag = 0
    
    with open(filename, mode='r') as f:
    	for line in f:
    		if line.strip() == "[COMMAND_LIST]": 
    			continue
    		
    		if line.strip() == "[VALID_COMMANDS]":
    			flag = 1
    			continue
    		
    		if flag==0: 
    			commands.add(line.strip())
    		
    		else: 
    			valid_commands.add(line.strip())

    command_list = commands.intersection(valid_commands)

    for command in command_list: 
    	queue.put(command)


def process_command_output(queue):
    # TODO: execute the command and put its data in the db
	# command = queue.get()
    while not queue.empty():
    	command = queue.get()
    	flag = 1
    	duration = 0
    	out = ""
    	count = 0

    	count = session.query(Command).filter(Command.command_string==command).count()

    	if count==0:
    		
    		start_time = time.time()
    		proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

    		try:
    			output, error = proc.communicate(timeout=60)

    		except:
    			flag=0
    			os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

    		if flag==1:
    			end_time = time.time()
    			duration = int(math.ceil(end_time - start_time))
    			command_data = Command(command, len(command), duration, output)
    			session.add(command_data)
    			session.commit()
    		
    		else:
    			output, error = proc.communicate()
    			command_data = Command(command, len(command), duration, output)
    			session.add(command_data)
    			session.commit()

