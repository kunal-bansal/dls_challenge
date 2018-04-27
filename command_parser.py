"""
Handles the work of validating and processing command input.
"""
import subprocess
import time
import math

from sqlalchemy import exists

from base import Command
from db import session



def get_valid_commands(queue, filename):
    # TODO: efficiently evaluate commands from filename passed
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
            if flag==0: commands.add(line.strip())
            else: valid_commands.add(line.strip())

    command_list = commands.intersection(valid_commands)

    for command in command_list:
        queue.put(command)

def process_command_output(queue):
    # TODO: execute the command and put its data in the db
    if not queue.empty():
        command = queue.get()
        flag = 0
        duration = 0
        out = ""
        count = 0
        count = session.query(Command).filter(command_string=command).count()
        if count==0:
            start_time = time.time()
            process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            while process.poll() is not None:
                if time.time()-start.time()>60.0:
                    flag = 1
                    break
            end_time = time.time()

            if flag==0: duration = int(math.ceil(end_time - start_time))
            
            while True:
                output = process.stdout.readline()
                if output == '':
                    break
                if output:
                    out += output

            command_data = Command(command, len(command), duration, out)
            session.add(command_data)
            session.commit()
