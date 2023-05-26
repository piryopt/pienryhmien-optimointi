from flask import Flask, render_template, request, redirect
from algorithms.hospital import hospital_algo
from tools import hospital_data_gen

app = Flask(__name__)
app.debug = True

import routes
