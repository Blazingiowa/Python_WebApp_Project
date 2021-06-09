from fileinput import filename
import flask
from flask import render_template, request
import os

def file_save(fs,dir):
    fs.save(os.path.join(dir,fs.filename))