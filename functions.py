from fileinput import close, filename
import flask
from flask import render_template, request
import os
import MySQLdb
import hashlib

def file_save(fs,dir):
    fs.save(os.path.join(dir,fs.filename))

def file_get(PATH):
    mp3_que=[]
    for filename in os.listdir(PATH):
        if os.path.isfile(os.path.join(PATH,filename)):
            mp3_que.append(filename)

    return mp3_que

#パスワードハッシュ化関数
def HashPassword(pass_str):
    hash_result=hashlib.sha256(pass_str.encode('utf-8')).hexdigest()

    return hash_result

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

        hs_passWD=HashPassword(row[2])
        print(hs_passWD)

        cur.close
        conn.close
        return hs_passWD