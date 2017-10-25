#coding=utf-8
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import sys
from flask import request,jsonify,send_from_directory,abort
import json
from flask import Response, request
import sys, os; sys.path.append(os.path.realpath("../"))
from super_models.device_model import Device
from super_models.database import Session
import json

UPLOAD_FOLDER = 'file'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','c','apk'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

super_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir,os.pardir))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload_capture_data', methods=['GET', 'POST'])
def upload_file():
    print 'enter upload'
    if request.method == 'POST':
        print 'enter post'
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            flod_path = super_path + '/files/capture_data'
            if not os.path.exists(flod_path):
                os.makedirs(flod_path)
            try:
                file.save(flod_path+'/'+filename)
            except Exception,e:
                re = {}
                re['msg'] = 'failed'
                re['code'] = 1
                resp = json.dumps(re)
                return Response(resp, mimetype='text/json')
            else:
                re = {}
                re['msg'] = 'success'
                re['code'] = 0
                resp = json.dumps(re)
                return Response(resp, mimetype='text/json')
    return '''
    <!doctype html>
    <title>upload capture data</title>
    <h1>upload capture data</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/reco', methods=['GET', 'POST'])
def upload_reco():
    print 'enter upload'
    if request.method == 'POST':
        print 'enter post'
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            flod_path = super_path + '/files/reco'
            anther_path = super_path + '/file/reco'
            if not os.path.exists(flod_path):
                os.makedirs(flod_path)
            if not os.path.exists(anther_path):
                os.makedirs(anther_path)
            try:
                file.save(flod_path+'/'+filename)
                file.save(anther_path + '/' + filename)
            except Exception,e:
                re = {}
                re['msg'] = 'failed'
                re['code'] = 1
                resp = json.dumps(re)
                return Response(resp, mimetype='text/json')
            else:
                re = {}
                re['msg'] = 'success'
                re['code'] = 0
                resp = json.dumps(re)
                return Response(resp, mimetype='text/json')
    return '''
    <!doctype html>
    <title>Upload reco</title>
    <h1>Upload reco</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/log', methods=['GET', 'POST'])
def upload_log():
    print 'enter upload'
    if request.method == 'POST':
        print 'enter post'
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            flod_path = super_path + '/files/log'
            if not os.path.exists(flod_path):
                os.makedirs(flod_path)
            try:
                file.save(flod_path+'/'+filename)
            except Exception,e:
                re = {}
                re['msg'] = 'failed'
                re['code'] = 1
                resp = json.dumps(re)
                return Response(resp, mimetype='text/json')
            else:
                re = {}
                re['msg'] = 'success'
                re['code'] = 0
                resp = json.dumps(re)
                return Response(resp, mimetype='text/json')
        else:
            print 'no file'
            re = {}
            re['msg'] = 'no file'
            re['code'] = 1
            resp = json.dumps(re)
            return Response(resp, mimetype='text/json')

    return '''
    <!doctype html>
    <title>Upload log</title>
    <h1>Upload log</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/script', methods=['GET', 'POST'])
def upload_script():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            flod_path = super_path + '/conversion_scripts'
            if not os.path.exists(flod_path):
                os.makedirs(flod_path)
            try:
                file.save(flod_path+'/'+filename)
            except Exception,e:
                re = {}
                re['msg'] = 'failed'
                re['code'] = 1
                resp = json.dumps(re)
                return Response(resp, mimetype='text/json')
            else:
                re = {}
                re['msg'] = 'success'
                re['code'] = 0
                resp = json.dumps(re)
                return Response(resp, mimetype='text/json')
        else:
            print 'no file'
            re = {}
            re['msg'] = 'no file'
            re['code'] = 1
            resp = json.dumps(re)
            return Response(resp, mimetype='text/json')
    return '''
    <!doctype html>
    <title>上传脚本</title>
    <h1>上传订单解析脚本</h1>
    <p>注意文件格式：'s_' + '设备号',如s_6201001000002.py </p>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/app', methods=['GET', 'POST'])
def upload_app():
    print 'enter upload'
    if request.method == 'POST':
        print 'enter post'
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            flod_path = super_path + '/files/app'
            if not os.path.exists(flod_path):
                os.makedirs(flod_path)
            try:
                file.save(flod_path+'/'+filename)
            except Exception,e:
                re = {}
                re['msg'] = 'failed'
                re['code'] = 1
                resp = json.dumps(re)
                return Response(resp, mimetype='text/json')
            else:
                re = {}
                re['msg'] = 'success'
                re['code'] = 0
                resp = json.dumps(re)
                return Response(resp, mimetype='text/json')
    return '''
    <!doctype html>
    <title>Upload app</title>
    <h1>Upload app</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/logo', methods=['GET', 'POST'])
def upload_logo():
    print 'enter upload'
    if request.method == 'POST':
        print 'enter post'
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)

            url = 'http://47.74.130.48:8005/files/logo/'+filename

            str_list = filename.split('_', 2)

            try:
                device_sn = str_list[0]
            except Exception,e:
                print 'file name discorrect'
                re = {}
                re['msg'] = 'file name discorrect'
                re['code'] = 2
                resp = json.dumps(re)
                return Response(resp, mimetype='text/json')


            session = Session()

            try:
                device = session.query(Device).filter_by(sn=device_sn).first()

                urls = device.logo_urls
                url_list = []
                if urls:
                    url_list = json.loads(urls)
                    url_list = filter(lambda x: x != url, url_list)
                    url_list.append(url)
                else:
                    url_list.append(url)

                device.logo_urls = json.dumps(url_list)
                device.logo_new = True

                session.commit()
            except Exception,e:
                session.rollback()
                print e
            finally:
                session.close()


            flod_path = super_path + '/files/logo'
            if not os.path.exists(flod_path):
                os.makedirs(flod_path)
            try:
                file.save(flod_path+'/'+filename)
            except Exception,e:
                re = {}
                re['msg'] = 'failed'
                re['code'] = 1
                resp = json.dumps(re)
                return Response(resp, mimetype='text/json')
            else:
                re = {}
                re['msg'] = 'success'
                re['code'] = 0
                resp = json.dumps(re)
                return Response(resp, mimetype='text/json')
    return '''
    <!doctype html>
    <title>Upload logo</title>
    <h1>Upload logo</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            try:
                file.save(sys.path[0]+'/file/'+filename)
            except Exception,e:
                print 'failed'
                print e
                return 'upload failed'
            else:
                re = {}
                re['msg'] = 'success'
                re['code'] = 0
                resp = json.dumps(re)
                return Response(resp, mimetype='text/json')
    return '''
    <!doctype html>
    <title>上传文件</title>
    <h1>上传文件入口</h1>
    <p>上传打印机Log：<a href='/log'>Log</a></p>
    <p>上传打印机APP：<a href='/app'>APP</a></p>
    <p>上传打印Logo：<a href='/logo'>Logo</a></p>
    <p>上传订单解析脚本：<a href='/script'>脚本</a></p>
    '''

@app.route('/restart', methods=['GET', 'POST'])
def restart():
    os.system('supervisorctl restart device')
    return 'success'

if __name__ == '__main__':
    print 'requset into'
    app.run(port=5005)