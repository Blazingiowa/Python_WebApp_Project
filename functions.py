from fileinput import close, filename
import flask
from flask import render_template, request
import os
import MySQLdb

def file_save(fs,dir):
    fs.save(os.path.join(dir,fs.filename))

def file_get(PATH):
    mp3_que=[]
    for filename in os.listdir(PATH):
        if os.path.isfile(os.path.join(PATH,filename)):
            mp3_que.append(filename)

    return mp3_que

#MySQL(mode->処理内容 data->sqlに必要な項目)
def mysql(mode,data):
    #接続
    conn = MySQLdb.connect(
        user = 'giveup_security',
        passwd = 'gbgb_security',
        host = 'localhost',
        db = 'webapp',
        charset = 'utf8'
    )

    #カーソルの取得
    cur = conn.cursor()

    #サインアップ
    if mode == 'signup':
        sql = 'select'
    #ログイン
    elif mode == 'login':
        sql = 'select * from user_info where mailaddr = ' + "'" + data + "'"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            break
        cur.close
        conn.close
        return row