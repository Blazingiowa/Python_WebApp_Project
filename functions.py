from fileinput import filename
import flask
from flask import render_template, request
import os

def file_save(fs,dir):
    fs.save(os.path.join(dir,fs.filename))

def file_get(PATH):
    mp3_que=[]
    for filename in os.listdir(PATH):
        if os.path.isfile(os.path.join(PATH,filename)):
            mp3_que.append(filename)

    return mp3_que