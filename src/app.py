from flask import Flask

app = Flask(__name__)

app.debug = True

import routes

if __name__ == '__main__':
    app.run()
