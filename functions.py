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
def MySQLData():
    con = MySQLdb.connect(
        user = 'giveup_security',
        passwd = 'gbgb_security',
        host = 'localhost',
        db = 'webapp',
        #charset = 'utf8'
    )

    return con

def mysql(mode,data):
    #接続
    con=MySQLData()

    #カーソルの取得
    cur = con.cursor()

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

        CloseDatabaseConnection(cur,con)
        return hs_passWD

def Array_manipulation(Path):
    ArrayName=[]
    for name in os.listdir(Path):
        if os.path.isfile(os.path.join(Path,name)):
            ArrayName.append(name)

    return ArrayName

def DataBaseManipulationGetNumberOfLikes(video_name):
    #データ取得のSQL
    GetAllFileNameSQL='SELECT * FROM video_info'
    #接続
    connection=MySQLData()
    #カーソル
    cursor=connection.cursor()

    cursor.execute(GetAllFileNameSQL)
    rows=cursor.fetchall()
    for index,re in enumerate(rows):
        if(re[1]==video_name):
            print("合致")
            CloseDatabaseConnection(cursor,connection)
            return re[2]

    #データベース検索しても動画が見つからなかったら、動画の名前といいねの数、0を挿入
    else:
        InsertVideoInfo="INSERT INTO video_info(video_name,number_of_likes) VALUES('"+video_name+"',0)"
        cursor.execute(InsertVideoInfo)
        connection.commit()
        
        CloseDatabaseConnection(cursor,connection)

        return 0

def CloseDatabaseConnection(cursor,connection):
    cursor.close
    connection.close