from crypt import methods
import flask
from flask import render_template, request, send_file,session
import os
import pathlib
import functions as fn
app=flask.Flask(__name__)
FILES_DIR='./static/mp4'
MP3_FILE_DIR='./static/mp3'
OTHER_FILE_DIR='./static/other'
MP3_PATH='/var/www/html/Web_File_SNS/static/mp3'
VIDEO_PATH='/var/www/html/Web_File_SNS/static/mp4'
OTHER_PATH='/var/www/html/Web_File_SNS/static/other'

app.secret_key = 'result'

ALLOWED_EXTENSIONS=['.mp3','.mp4','.jpg','.png']
#Function
    
#APP_Route
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup',methods=["POST"])
def signup():
    userdata = []
    userdata.append(request.form['username'])
    userdata.append(fn.HashPassword(request.form['password']))
    userdata.append(request.form['email'])

    resultdata = fn.SignupMyaccount(userdata)

    if resultdata == "success": 
        MP3_files=[]
        MP4_files=[]
        for filename in os.listdir(MP3_PATH):
            if os.path.isfile(os.path.join(MP3_PATH,filename)):
                MP3_files.append(filename)

        for mp4files in os.listdir(VIDEO_PATH):
            if os.path.isfile(os.path.join(VIDEO_PATH,mp4files)):
                MP4_files.append(mp4files)
        return render_template('index.html',music=MP3_files,video=MP4_files)
    else:
        return render_template('result.html',message = "そのメールアドレスは既に使用されています")

@app.route('/login',methods=["POST"])
def login():
    email = request.form['email']

    #emailを元にユーザー検索しパスワードを取得
    userdata = fn.LoginMypage(email)

    #ハッシュ化処理
    password = fn.HashPassword(request.form['password'])

    #パスワードが一致するかどうか
    if password == userdata:
        files=[]
        videoes=[]
        files=fn.Array_manipulation(MP3_PATH)
        videoes=fn.Array_manipulation(VIDEO_PATH)
        
        connection=fn.MySQLData()
        cursor=connection.cursor()

        sql='SELECT * FROM user_info WHERE password='+"'"+password+"'"
        cursor.execute(sql)

        
        result=cursor.fetchall()
        session["result"] = result

        return render_template('index.html',file=files,video=videoes)
    else:
        return render_template('result.html',message="メールアドレスまたはパスワードが違います")
        
@app.route('/home')
def home():
    MP3_files=[]
    MP4_files=[]
    for filename in os.listdir(MP3_PATH):
        if os.path.isfile(os.path.join(MP3_PATH,filename)):
            MP3_files.append(filename)

    for mp4files in os.listdir(VIDEO_PATH):
        if os.path.isfile(os.path.join(VIDEO_PATH,mp4files)):
            MP4_files.append(mp4files)
    return render_template('index.html',music=MP3_files,video=MP4_files)

@app.route('/download')
def download():
    MP3_files=[]
    MP4_files=[]
    OTHER_files=[]

    for files_name_ichiran in os.listdir(MP3_PATH):
        if os.path.isfile(os.path.join(MP3_PATH,files_name_ichiran)):
            MP3_files.append(files_name_ichiran)
    
    for file_name_MP4 in os.listdir(VIDEO_PATH):
        if os.path.isfile(os.path.join(VIDEO_PATH,file_name_MP4)):
            MP4_files.append(file_name_MP4)

    for file_name_other in os.listdir(OTHER_PATH):
        if os.path.isfile(os.path.join(OTHER_PATH,file_name_other)):
            OTHER_files.append(file_name_other)

    return render_template('download.html',music=MP3_files,video=MP4_files,other=OTHER_files)

@app.route('/upload_fttb',methods=['POST'])
def upload_fttb():
    if 'upfile' not in flask.request.files:
        return 'file not selected'
    fs=flask.request.files['upfile']
    suffix=pathlib.Path(fs.filename).suffix

    if suffix=='.mp4':
        fn.file_save(fs,FILES_DIR)
    elif suffix=='.mp3' or suffix=='.wav':
        fn.file_save(fs,MP3_FILE_DIR)
    else:
        fn.file_save(fs,OTHER_FILE_DIR)

    return render_template("upload.html")

@app.route('/download_fttb',methods=['POST'])
def download_fttb():
    
    videoname = request.form['taihi_name']

    files_que=[]
    for files_name_ichiran in os.listdir(MP3_PATH):
        if os.path.isfile(os.path.join(MP3_PATH,files_name_ichiran)):
            files_que.append(files_name_ichiran)
    
    for file_name_MP4 in os.listdir(VIDEO_PATH):
        if os.path.isfile(os.path.join(VIDEO_PATH,file_name_MP4)):
            files_que.append(file_name_MP4)

    for file_name_other in os.listdir(OTHER_PATH):
        if os.path.isfile(os.path.join(OTHER_PATH,file_name_other)):
            files_que.append(file_name_other)

    for Fname in files_que:
        if Fname == videoname:
            file_ex = os.path.splitext(Fname)
            break
        
    if file_ex[1] =='.mp4':
        downloadFile = FILES_DIR + '/' + videoname
    elif file_ex[1] == '.mp3':
        downloadFile = MP3_FILE_DIR + '/' + videoname
    else:
        downloadFile = OTHER_FILE_DIR + '/' + videoname

    return send_file(downloadFile, as_attachment=True)


@app.route('/video',methods=['POST'])
def video():
    video_name=request.form.get('video-name')
    #いいねの数取得
    NumberOfLikes=fn.DataBaseManipulationGetNumberOfLikes(video_name[14:])
    #動画のコメント取得
    video_comment_arry=fn.GetAllVideoComments(video_name[14:])

    return render_template('video.html',video_name=video_name,NumberOfLikes=NumberOfLikes,videocomments=video_comment_arry)

@app.route('/trending')
def trending():
    videoes_fttb=[]
    for mp4files in os.listdir(VIDEO_PATH):
        if os.path.isfile(os.path.join(VIDEO_PATH,mp4files)):
            videoes_fttb.append(mp4files)
    video_path_string='../static/mp4/'+str(videoes_fttb[0])

    return render_template('video.html',video_name=video_path_string)

@app.route('/uploads')
def uploads():
    video_files=[]
    for filename in os.listdir(MP3_PATH):
        if os.path.isfile(os.path.join(MP3_PATH,filename)):
            video_files.append(filename)

    for mp4files in os.listdir(VIDEO_PATH):
        if os.path.isfile(os.path.join(VIDEO_PATH,mp4files)):
            video_files.append(mp4files)

    for otherfiles in os.listdir(OTHER_PATH):
        if os.path.isfile(os.path.join(OTHER_PATH,otherfiles)):
            video_files.append(otherfiles)
            
    return render_template('upload.html',video=video_files)

@app.route('/music')
def music():
    music_list=fn.file_get(MP3_FILE_DIR)
    return render_template('musicplayer.html',music=music_list)

@app.route('/likes',methods=['POST'])
def likes():
    NumberOfLikes=request.form['number_of_likes']
    VideoName=request.form['videoname']
    #データベース更新処理
    fn.UpdateDataBaseCountUpNumberOfLikes(NumberOfLikes,VideoName)
    return NumberOfLikes

@app.route('/comments',methods=['POST'])
def comments():
    PostedComments=request.form['comment']
    videoname=request.form['videoname']
    date=request.form['date']

    video_id=fn.GetVideoId(videoname)

    fn.DataBaseManipulationInsertVideoComments(PostedComments,videoname,date,video_id[0][0])

    return PostedComments

@app.route('/delete',methods=['POST'])
def delete():
    video_name=request.form['videoname']
    comtext=request.form['comment']

    fn.DeleteData(video_name,comtext)

    return "Complete"

@app.route('/mypage')
def mypage():
    result = session["result"]

    return render_template('mypage.html',sqlresult=result)


@app.route('/member')
def member():
    return render_template('member.html')

@app.route('/following')
def following():
    result = session["result"]

    return render_template('following.html',sqlresult=result)

@app.route('/followers')
def followers():
    result = session["result"]

    return render_template('followers.html',sqlresult=result)

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')

