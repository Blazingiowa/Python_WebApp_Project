from crypt import methods
from fileinput import filename
import flask
from flask import render_template, request, send_file
import os,json,time
import pathlib
import functions as fn
app=flask.Flask(__name__)
FILES_DIR='./static/mp4'
MP3_FILE_DIR='./static/mp3'
OTHER_FILE_DIR='./static/other'
MP3_PATH='/var/www/html/Web_File_SNS/static/mp3'
VIDEO_PATH='/var/www/html/Web_File_SNS/static/mp4'
OTHER_PATH='/var/www/html/Web_File_SNS/static/other'

ALLOWED_EXTENSIONS=['.mp3','.mp4','.jpg','.png']
#Function
    
#APP_Route
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup',methods=["POST"])
def signup():
    username = request.form['username']
    return render_template('login.html')

@app.route('/login',methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    mode = 'login'
    userdata = fn.mysql(mode,email)
    if password == userdata[2]:
        files=[]
        videoes=[]
        for filename in os.listdir(MP3_PATH):
            if os.path.isfile(os.path.join(MP3_PATH,filename)):
                files.append(filename)

        for mp4files in os.listdir(VIDEO_PATH):
            if os.path.isfile(os.path.join(VIDEO_PATH,mp4files)):
                videoes.append(mp4files)
        return render_template('index.html',file=files,video=videoes)
    else:
        return render_template('login.html')
        
"""
@app.route('/')
def index():
    files=[]
    videoes=[]
    for filename in os.listdir(MP3_PATH):
        if os.path.isfile(os.path.join(MP3_PATH,filename)):
            files.append(filename)

    for mp4files in os.listdir(VIDEO_PATH):
        if os.path.isfile(os.path.join(VIDEO_PATH,mp4files)):
            videoes.append(mp4files)
            print(mp4files)
    return render_template('index.html',file=files,video=videoes)
    """

@app.route('/download')
def download():
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

    print(files_que)

    return render_template('download.html',video =files_que)

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
    #fs.save(os.path.join(FILES_DIR,fs.filename))
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
            print("ファイル拡張子：",file_ex[1])
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
    print(video_name)
    return render_template('video.html',video_name=video_name)

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
    return render_template('upload.html')

@app.route('/music')
def music():
    music_list=fn.file_get(MP3_FILE_DIR)
    print(music_list)
    return render_template('musicplayer.html',music=music_list)

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')
