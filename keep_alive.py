"""
Authors: Daniela Cislaru, Elmira Moayedi
"""

__author__ = 'Daniela Cislaru, Elmira Moayedi'


from flask import Flask
from threading import Thread


app = Flask('')


@app.route('/')
def home():
    """
    Handler for the root URL ('/').
    Returns a simple message indicating that the server is alive.
    """
    return "Hello. I am alive!"

def run():
    """
    Function to start the Flask server.
    """
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)


def keep_alive():
    """
    Function to keep the Flask server running in the background.
    Starts a new thread to execute the 'run' function.
    """

    server = Thread(target=run)
    server.start()


