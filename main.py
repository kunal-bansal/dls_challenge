# from flask import Flask

from multiprocessing import Process, Queue
import sys
from flask import Flask, request, jsonify
from flask_swagger import swagger
from sqlalchemy import inspect

from collections import OrderedDict
import json

from base import Base, Command
from db import session, engine
from command_parser import get_valid_commands, process_command_output

app = Flask(__name__)

@app.route('/commands', methods=['GET'])
def get_command_output():
    commands = session.query(Command).all()
    result = []
    for obj in commands:
        result.append({c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs})
    for row in result:
        row['output'] = row['output'].decode('UTF-8')
        del(row['id'])
    return jsonify(result)


@app.route('/commands', methods=['POST'])
def process_commands():
    filename = request.form['filename']
    queue = Queue()
    get_valid_commands(queue, filename)
    processes = [Process(target=process_command_output, args=(queue,)) for num in range(2)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    return 'Successfully processed commands.'+'\n'

@app.route('/database', methods=['POST'])
def make_db():
	Base.metadata.create_all(engine)
	return 'Database creation successful.'+'\n'

@app.route('/database', methods=['DELETE'])
def drop_db():
	Base.metadata.drop_all(engine)
	return 'Database deletion successful.'+'\n'


@app.route('/spec', methods=['GET'])
def swagger_spec():
    spec = swagger(app)
    spec['info']['title'] = "Intel AI DLS coding challenge API"
    spec['info']['description'] = ("Intel AI deep learning systems coding " + "challenge for interns and full-time hires")
    spec['info']['license'] = { "name": "Intel Proprietary License", "url": "https://ai.intel.com",}
    spec['info']['contact'] = { "name": "Intel DLS Team", "url": "https://ai.intel.com", "email": "scott.leishman@intel.com",}
    spec['schemes'] = ['http']
    spec['tags'] = [{"name": "db", "description": "database actions (create, delete)"}, {"name": "commands", "description": "process and retrieve commands"}]
    return jsonify(spec)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

