# ------------------------ IMPORTS ----------------------------- #
# Libraries
from threading import Thread
from multiprocessing import Process
import sys
import os
from time import sleep
import logging

# locals
from app import create_app

# ------------------------ HELPER FUNCTIONS ----------------------------- #
def run_server():
  # We indicate to raise a testing server
  app = create_app('test')

  # We disable the logs from the server
  log = logging.getLogger('werkzeug')
  log.disabled = True

  # Start the server
  app.run()


def run_tests():
  # We wait 10 seconds in order to server start
  sleep(1)

  # We run the tests
  os.system('python tests/run.py -v')

# ------------------------ SET-UP ----------------------------- #
# start the server with the 'run()' method
if __name__ == '__main__':
  # We only use a maximum of 2 arguments
  if (len(sys.argv) > 2):
    raise ValueError('Too many arguments.')
  else:
    if len(sys.argv) == 2:
      if (sys.argv[1] == '--testing'):
        # 
        server_thread = Process(target=run_server)
        tests_thread = Thread(target=run_tests)

        # We start the threads
        server_thread.start()
        tests_thread.start()

        # We wait for testing to finish in order to terminate our server
        tests_thread.join()
        server_thread.terminate()
        
      else:
        raise ValueError('Invalid argument.')
    else:
      # We use the default configuration and run the server
      app = create_app()
      app.run(debug=True)