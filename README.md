# Intel Deep Learning Systems Coding Challenge #

## Running the server ##
1. Navigate to the project directory and type `make run_container` to build and start the service inside a container.

2. Once the docker server is running:
 - Create the database using:
     'curl -X POST http://0.0.0.0:5000/database'
 
 - Sample requests to feed in data from a file: 
     'curl -F "filename=commands.txt" http://0.0.0.0:5000/commands'
     'curl -F "filename=commands_test_1.txt" http://0.0.0.0:5000/commands'
 
 - Check metadata present in provided db using:
     'curl http://0.0.0.0:5000/commands'

## Implementation Specifics ##
Every command list file is UTF-8 plain-text formatted into two sections denoted by the headers `COMMAND_LIST` and `VALID_COMMANDS`.
The former are the list of command strings to be executed (one per line), and the latter represent the list of valid command strings
  - There must be an exact, case-sensitive match of the entire command list command string in the valid command section for it to be considered "valid" and available for execution.
  - Invalid commands are ignored.
  - The files provided for testing are "commands.txt", "commands_test_1.txt", "commands_test_2.txt", "commands_test_3.txt", "commands_test_4.txt" but the solution accepts other files as input as well that are of the same structure.
  - Each file is independent and self-validating; i.e. the `VALID_COMMANDS` section of one file doesn't affect what's valid in another file.
  - The solution assumes filename `commands.txt` file no longer fits in memory.
  - The solution makes the command executions non-blocking.
  
  - For every valid command, it is executed and the solution stores the following meta-data in the db:
      - actual command itself as a string
      - length of command string
      - time to complete (if the command takes > 1 minute to complete, mark a 0 value which will represent a "long running or not finished" scenario).
      - stdout output from executing the command, for all commands that either complete execution or timeout.
  
  - The command meta-data is persisted in the db provided.
  - Users can query the command meta-data that has been stored to date by hitting the endpoint specified in the code with a GET call.
  - Duplicate commands are not stored.
 
