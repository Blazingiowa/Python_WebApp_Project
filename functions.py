import os
import MySQLdb
import hashlib

from MySQLdb import connections

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

#MySQLに接続する関数
def MySQLData():
    con = MySQLdb.connect(
        user = 'giveup_security',
        passwd = 'gbgb_security',
        host = 'localhost',
        db = 'webapp',
        #charset = 'utf8'
    )
    return con

#MySQLから切断する関数
def CloseDatabaseConnection(cursor,connection):
    cursor.close
    connection.close

def SignupMyaccount(userdata):
    try:
        con = MySQLData()
        cur = con.cursor()
        sql = 'insert into user_info(username,password,mailaddr) values(%s,%s,%s)'
        cur.execute(sql,userdata)
        con.commit()
    except Exception as e:
        return e
    
    CloseDatabaseConnection(cur,con)
    return "success"

def LoginMypage(data):
    con = MySQLData()
    cur = con.cursor()

    #mailaddrを元にユーザー検索
    sql = 'select * from user_info where mailaddr = ' + "'" + data + "'"
    cur.execute(sql)
    #引っ張ってきたデータを取得
    rows = cur.fetchall()
    if(rows == None):
        return "none"
    for row in rows:
        break

    CloseDatabaseConnection(cur,con)
    return row[2]

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

    #いいねの数取得のための検索
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

def UpdateDataBaseCountUpNumberOfLikes(likes,video):
    #DB接続
    connection=MySQLData()
    cursor=connection.cursor()

    UpdateNumberOfLikesSQL='UPDATE video_info SET number_of_likes='+likes+' WHERE video_name="'+video+'"'

    cursor.execute(UpdateNumberOfLikesSQL)
    connection.commit()

    CloseDatabaseConnection(cursor,connection)

def DataBaseManipulationInsertVideoComments(comment,video_name,date,video_id):
    #DB接続
    connection=MySQLData()
    cursor=connection.cursor()

    InsertVideoCommentSQL='INSERT INTO video_comments(video_id,video_name,comment,comdate) VALUES('+str(video_id)+',"'+video_name+'","'+comment+'","'+date+'")'
    cursor.execute(InsertVideoCommentSQL)
    connection.commit()

    CloseDatabaseConnection(cursor,connection)

def GetAllVideoComments(videoname):
    #DB接続
    conection=MySQLData()
    cursor=conection.cursor()

    GetAllComentsSQL='SELECT comment,comdate FROM video_comments WHERE video_name="'+videoname+'"'
    cursor.execute(GetAllComentsSQL)

    rows=cursor.fetchall()

    CloseDatabaseConnection(cursor,conection)

    return rows

def GetVideoId(video_name):
    con=MySQLData()
    cur=con.cursor()

    GetIdSQL="SELECT video_id from video_info WHERE video_name='"+video_name+"'"
    cur.execute(GetIdSQL)

    result=cur.fetchall()

    CloseDatabaseConnection(cur,con)

    return result

def DeleteData(video_name,comtext):
    con=MySQLData()
    cur=con.cursor()

    DeleteSQL='DELETE FROM video_comments WHERE video_name="'+video_name+'" AND comment="'+comtext+'"'

    cur.execute(DeleteSQL)
    con.commit()

    CloseDatabaseConnection(cur,con)

def CloseDatabaseConnection(cursor,connection):
    cursor.close
    connection.close