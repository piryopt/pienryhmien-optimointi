from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello_world() -> str:
    """
    Returns the rendered skeleton template
    """
    return render_template('index.html')

